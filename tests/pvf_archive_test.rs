//! End-to-end tests of the Script.pvf reader.
//!
//! The fixtures are built at run time by [`PvfBuilder`], which writes a real
//! (tiny) archive: same header layout, same obfuscation, same directory tree.
//! That keeps the tests independent from any `Script.pvf` on disk while still
//! exercising the whole read path.

use pvf_parser_rs::error::PvfError;
use pvf_parser_rs::parser::binary_item::BinaryItem;
use pvf_parser_rs::parser::pvf_encoding::PVFEncoding;
use pvf_parser_rs::parser::pvf_reader::{
    PVFReader, decrypt_bytes, decrypt_in_place, encrypt_bytes,
};
use pvf_parser_rs::parser::utils::guess_encoding;

// ---------------------------------------------------------------- fixtures

/// Minimal writer for the archive format.
struct PvfBuilder {
    files: Vec<(String, Vec<u8>)>,
}

impl PvfBuilder {
    fn new() -> Self {
        Self { files: Vec::new() }
    }

    fn file(mut self, path: &str, content: impl Into<Vec<u8>>) -> Self {
        self.files.push((path.to_string(), content.into()));
        self
    }

    /// Serialise the archive exactly like the game client does.
    fn build(self) -> Vec<u8> {
        let mut tree = Vec::new();
        let mut payloads = Vec::new();
        let mut offset = 0u32;

        for (index, (path, content)) in self.files.iter().enumerate() {
            // any value works as a key, the reader only uses it to decrypt
            let crc = 0x1000 + index as u32 * 7;

            let mut padded = content.clone();
            while padded.len() % 4 != 0 {
                padded.push(0);
            }
            let encrypted = encrypt_bytes(padded, crc);

            tree.extend_from_slice(&(index as u32).to_le_bytes());
            tree.extend_from_slice(&(path.len() as u32).to_le_bytes());
            tree.extend_from_slice(path.as_bytes());
            tree.extend_from_slice(&(content.len() as u32).to_le_bytes());
            tree.extend_from_slice(&crc.to_le_bytes());
            tree.extend_from_slice(&offset.to_le_bytes());

            offset += encrypted.len() as u32;
            payloads.extend_from_slice(&encrypted);
        }

        while tree.len() % 4 != 0 {
            tree.push(0);
        }

        let tree_crc = 0xDEAD_BEEF;
        let tree = encrypt_bytes(tree, tree_crc);

        let uuid = b"00000000-0000-0000-0000-000000000000";
        let mut out = Vec::new();
        out.extend_from_slice(&(uuid.len() as u32).to_le_bytes());
        out.extend_from_slice(uuid);
        out.extend_from_slice(&1u32.to_le_bytes()); // version
        out.extend_from_slice(&(tree.len() as u32).to_le_bytes());
        out.extend_from_slice(&tree_crc.to_le_bytes());
        out.extend_from_slice(&(self.files.len() as u32).to_le_bytes());
        out.extend_from_slice(&tree);
        out.extend_from_slice(&payloads);
        out
    }

    /// Write the archive to a temporary file and return the reader.
    fn open(self) -> PVFReader {
        let bytes = self.build();
        let path = temp_path();
        std::fs::write(&path, bytes).unwrap();
        PVFReader::open(&path, PVFEncoding::GBK).unwrap()
    }
}

fn temp_path() -> std::path::PathBuf {
    use std::sync::atomic::{AtomicUsize, Ordering};
    static COUNTER: AtomicUsize = AtomicUsize::new(0);
    let index = COUNTER.fetch_add(1, Ordering::Relaxed);
    let dir = std::env::temp_dir().join(format!("pvf-tests-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    dir.join(format!("archive-{index}.pvf"))
}

/// Build a `stringtable.bin` payload from `strings`.
fn string_table(strings: &[&str]) -> Vec<u8> {
    let count = strings.len() as u32;
    let data_start = 4 * (count as usize + 1);

    let mut offsets = Vec::new();
    let mut data = Vec::new();
    for string in strings {
        offsets.push((data_start + data.len()) as u32);
        data.extend_from_slice(string.as_bytes());
    }
    offsets.push((data_start + data.len()) as u32);

    let mut buf = count.to_le_bytes().to_vec();
    for offset in offsets {
        buf.extend_from_slice(&offset.to_le_bytes());
    }
    buf.extend_from_slice(&data);
    buf
}

/// Payload marker shared by every file of the archive.
const MARKER: [u8; 2] = [0xB0, 0xD0];

fn token_int(value: i32) -> Vec<u8> {
    let mut buf = vec![2];
    buf.extend_from_slice(&value.to_le_bytes());
    buf
}

fn token_segment(string_index: u32) -> Vec<u8> {
    let mut buf = vec![5];
    buf.extend_from_slice(&string_index.to_le_bytes());
    buf
}

fn token_string(string_index: u32) -> Vec<u8> {
    let mut buf = vec![7];
    buf.extend_from_slice(&string_index.to_le_bytes());
    buf
}

fn token_dict_string(dict_index: u32, key_index: u32) -> Vec<u8> {
    let mut buf = vec![9];
    buf.extend_from_slice(&dict_index.to_le_bytes());
    buf.push(10); // nested key token type
    buf.extend_from_slice(&key_index.to_le_bytes());
    buf
}

// ------------------------------------------------------------------- tests

#[test]
fn crypto_round_trip() {
    let data = vec![1u8, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    let encrypted = encrypt_bytes(data.clone(), 12345);
    assert_eq!(decrypt_bytes(encrypted.clone(), 12345), data);
    assert_ne!(encrypt_bytes(data, 12345), vec![0u8; 12]);

    // The in-place variant must agree with the allocating one.
    let mut in_place = encrypted;
    decrypt_in_place(&mut in_place, 12345);
    assert_eq!(in_place, vec![1u8, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
}

#[test]
fn decrypt_ignores_a_trailing_partial_lane() {
    // Payloads are 4 byte aligned, but malformed input must not panic or
    // corrupt the leftover bytes.
    let mut buf = vec![0u8; 5];
    decrypt_in_place(&mut buf, 7);
    assert_eq!(buf.len(), 5);
    assert_eq!(buf[4], 0);
}

#[test]
fn reads_header_and_files() {
    let reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["[name]"]))
        .file("a/b.txt", b"hello world".to_vec())
        .file("a/c.bin", vec![0u8; 9])
        .open();

    assert_eq!(reader.file_count(), 3);
    assert_eq!(reader.uuid(), "00000000-0000-0000-0000-000000000000");
    assert_eq!(reader.version(), 1);
    assert!(reader.exists("A/B.TXT"));
    assert!(!reader.exists("nope"));

    // the payload is padded to 4 bytes in the archive but must read back exactly
    assert_eq!(reader.read_file("a/b.txt").unwrap(), b"hello world");
    assert_eq!(reader.read_file("a/c.bin").unwrap(), vec![0u8; 9]);
}

#[test]
fn lists_and_filters_files() {
    let reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["x"]))
        .file("equipment/a.equ", vec![1, 2, 3, 4])
        .file("equipment/b.equ", vec![5, 6, 7, 8])
        .file("stackable/c.stk", vec![9, 10, 11, 12])
        .open();

    assert_eq!(
        reader.list_files("equipment/", ".equ", None),
        vec!["equipment/a.equ", "equipment/b.equ"]
    );
    assert_eq!(reader.list_files("", ".equ", Some(1)).len(), 1);
    assert_eq!(reader.directories(), vec!["equipment", "stackable"]);

    let stats = reader.stats();
    assert_eq!(stats.files, 4);
    assert_eq!(stats.by_suffix.get("equ"), Some(&2));
}

#[test]
fn missing_file_is_an_error() {
    let reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["x"]))
        .open();

    let err = reader.read_file("does/not/exist").unwrap_err();
    assert!(matches!(err, PvfError::FileNotFound(_)), "{err}");
}

#[test]
fn tokenizes_payloads() {
    let mut content = MARKER.to_vec();
    content.extend(token_int(42));
    content.extend(token_segment(0)); // [name]
    content.extend(token_string(1)); // "hero"

    let mut reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["[name]", "hero"]))
        .file("a.equ", content)
        .open();

    let items = reader.read_file_as_list("a.equ").unwrap();
    assert_eq!(items.len(), 3);
    assert!(matches!(items[0], BinaryItem::Int(42)));
    assert!(matches!(&items[1], BinaryItem::Segment(s) if s == "[name]"));
    assert!(matches!(&items[2], BinaryItem::String(s) if s == "hero"));

    assert_eq!(
        reader.read_file_as_dict("a.equ").unwrap(),
        vec![("[name]".to_string(), "hero".to_string())]
    );
}

#[test]
fn resolves_indirect_strings() {
    // token type 9 -> n_string.lst -> *.str dictionary
    let mut content = MARKER.to_vec();
    content.extend(token_dict_string(0, 1)); // dict 0, key "name_1"

    let mut lst = MARKER.to_vec();
    lst.extend(token_int(0));
    lst.extend(token_string(0)); // -> "dict/test.str"

    let mut reader = PvfBuilder::new()
        .file(
            "stringtable.bin",
            string_table(&["dict/test.str", "name_1", "[name]"]),
        )
        .file("n_string.lst", lst)
        .file(
            "dict/test.str",
            "name_1>some name\nother>x".as_bytes().to_vec(),
        )
        .file("a.equ", content)
        .open();

    let items = reader.read_file_as_list("a.equ").unwrap();
    assert_eq!(items.len(), 1);
    assert!(matches!(&items[0], BinaryItem::String(s) if s == "some name"));
}

#[test]
fn loads_lst_files() {
    let mut lst = MARKER.to_vec();
    lst.extend(token_int(100));
    lst.extend(token_string(0)); // "a.equ"
    lst.extend(token_int(101));
    lst.extend(token_string(1)); // "b.equ"

    let mut reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["a.equ", "b.equ"]))
        .file("equipment/equipment.lst", lst)
        .open();

    let lst = reader.load_lst_file("equipment/equipment.lst").unwrap();
    assert_eq!(lst.len(), 2);
    assert_eq!(lst.get_item(100), "a.equ");
    assert_eq!(
        lst.resolved_entries(),
        vec![
            (100, "equipment/a.equ".to_string()),
            (101, "equipment/b.equ".to_string())
        ]
    );
}

#[test]
fn extracts_files_to_disk() {
    let mut reader = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["x"]))
        .file("a/b.txt", b"content".to_vec())
        .open();

    let dest = std::env::temp_dir().join(format!("pvf-extract-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&dest);

    let report = reader.extract_all(&dest, "a/", ".txt");
    assert_eq!(report.files, 1);
    assert!(report.failed.is_empty());
    assert_eq!(std::fs::read(dest.join("a/b.txt")).unwrap(), b"content");
}

#[test]
fn rejects_broken_archives() {
    let bytes = PvfBuilder::new()
        .file("stringtable.bin", string_table(&["x"]))
        .build();

    let path = temp_path();
    std::fs::write(&path, &bytes[..10]).unwrap();
    assert!(PVFReader::open(&path, PVFEncoding::GBK).is_err());

    std::fs::write(&path, b"not a pvf at all").unwrap();
    assert!(PVFReader::open(&path, PVFEncoding::GBK).is_err());

    assert!(PVFReader::open("/definitely/not/here.pvf", PVFEncoding::GBK).is_err());
}

#[test]
fn missing_string_table_is_reported() {
    let bytes = PvfBuilder::new().file("a.txt", vec![1, 2, 3, 4]).build();
    let path = temp_path();
    std::fs::write(&path, bytes).unwrap();

    let err = PVFReader::open(&path, PVFEncoding::GBK).unwrap_err();
    assert!(matches!(err, PvfError::FileNotFound(_)), "{err}");
}

#[test]
fn guesses_the_encoding_of_a_payload() {
    // "高级装扮" in GBK vs BIG5
    let gbk = vec![0xB8, 0xDF, 0xBC, 0xB6, 0xD7, 0xB0, 0xB0, 0xE7];
    assert_eq!(guess_encoding(&[gbk]), PVFEncoding::GBK);

    // "高級裝扮" in BIG5
    let big5 = vec![0xB0, 0xAA, 0xAF, 0xC5, 0xB8, 0xCB, 0xA7, 0x5E];
    assert_eq!(guess_encoding(&[big5]), PVFEncoding::BIG5);
}
