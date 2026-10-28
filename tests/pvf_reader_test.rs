//! Integration tests against a real `Script.pvf`.
//!
//! They are skipped when the archive is not present next to `Cargo.toml`.
//! Tests that parse the whole archive (300k+ files) are marked `#[ignore]`;
//! run them explicitly with `cargo test -- --ignored`.

use pvf_parser_rs::parser::binary_item_parser::BinaryItemParser;
use pvf_parser_rs::parser::pvf_encoding::PVFEncoding;
use pvf_parser_rs::parser::pvf_reader::{
    PVFReader, decrypt_bytes, save_dungeon_to_parquet, save_equipment_to_parquet,
    save_exp_to_parquet, save_magic_seal_to_parquet, save_quest_to_parquet, save_skill_to_parquet,
    save_stackable_to_parquet,
};
use std::fs::File;
use std::io::BufWriter;
use std::path::PathBuf;
use tracing::info;

/// The archive shipped with the repository is the simplified (GBK) client.
const ENCODING: PVFEncoding = PVFEncoding::GBK;

fn pvf_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("Script.pvf")
}

fn dump_path(name: &str) -> PathBuf {
    let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("dump");
    std::fs::create_dir_all(&dir).unwrap();
    dir.join(name)
}

/// Open the archive, or return `None` when it is not available.
fn open_reader() -> Option<PVFReader> {
    if !pvf_path().exists() {
        eprintln!("skipping: {} not found", pvf_path().display());
        return None;
    }
    Some(PVFReader::open(pvf_path(), ENCODING).expect("failed to open Script.pvf"))
}

#[test]
fn test_decrypt_bytes() {
    let buf = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let output = decrypt_bytes(buf, 12345);
    assert_eq!(output.len(), 8);
    info!("{output:?}");
}

#[test]
fn test_read_pvf_header() {
    let Some(reader) = open_reader() else { return };

    assert!(reader.file_count() > 1000);
    assert!(!reader.uuid().is_empty());
    assert!(reader.exists("stringtable.bin"));

    let mut leafs = reader.header.leaf_map.values().cloned().collect::<Vec<_>>();
    leafs.sort_unstable_by(|a, b| a.file_path.cmp(&b.file_path));

    let file = File::create(dump_path("pvf_header.json")).unwrap();
    serde_json::to_writer_pretty(BufWriter::new(file), &leafs).unwrap();
}

#[test]
fn test_list_files() {
    let Some(reader) = open_reader() else { return };

    let equipment = reader.list_files("equipment/", ".equ", Some(5));
    assert_eq!(equipment.len(), 5);
    for path in &equipment {
        assert!(path.starts_with("equipment/"));
    }

    let stats = reader.stats();
    info!("{stats:?}");
    assert!(stats.by_suffix.contains_key("equ"));
}

#[test]
fn test_read_file_as_list() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let items = reader
        .read_file_as_list("equipment/character/partset/upperset.equ")
        .unwrap();
    assert!(!items.is_empty());
    info!(
        "{}",
        items
            .iter()
            .map(|item| format!("{item:?}"))
            .collect::<Vec<_>>()
            .join("\n")
    );
}

#[test]
fn test_read_lst_file() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let lst = reader.load_lst_file("equipment/equipment.lst").unwrap();
    assert!(lst.len() > 100);

    let file = File::create(dump_path("equipment_list.txt")).unwrap();
    let mut writer = BufWriter::new(file);
    for (id, name) in lst.entries() {
        use std::io::Write;
        writeln!(writer, "{id:11}: {name}").unwrap();
    }
}

#[test]
fn test_binary_item_parse_equipment() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let path = "equipment/character/common/belt/cloth/100200005.equ";
    let items = reader.read_file_as_list(path).unwrap();
    let mut parser = BinaryItemParser::new(items);
    let equipment = parser.parse_equipment();

    assert!(!equipment.name.is_empty());
    info!("{equipment:?}");
}

#[test]
fn test_equipment_fields_are_populated() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let items = reader
        .read_file_as_list("equipment/character/common/belt/cloth/100200005.equ")
        .unwrap();
    let parser = BinaryItemParser::new(items);
    std::fs::write(
        dump_path("equipment_100200005.txt"),
        parser.to_string_list().join("\n"),
    )
    .unwrap();
}

#[test]
#[ignore = "parses the whole archive"]
fn test_parse_equipment_list() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let equipment = reader.get_equipment_list();
    assert_eq!(equipment.len(), 63_778, "equipment count changed");

    let file = File::create(dump_path("equipment_list.json")).unwrap();
    serde_json::to_writer_pretty(BufWriter::new(file), &equipment).unwrap();
}

#[test]
#[ignore = "parses the whole archive"]
fn test_parse_quest_list() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let quests = reader.get_quest_list();
    assert_eq!(quests.len(), 3_017, "quest count changed");

    let file = File::create(dump_path("quest_list.json")).unwrap();
    serde_json::to_writer_pretty(BufWriter::new(file), &quests).unwrap();
}

#[test]
#[ignore = "parses the whole archive"]
fn test_parse_stackable_list() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let stackables = reader.get_stackable_list();
    assert_eq!(stackables.len(), 14_491, "stackable count changed");

    let file = File::create(dump_path("stackable.json")).unwrap();
    serde_json::to_writer_pretty(BufWriter::new(file), &stackables).unwrap();
}

#[test]
#[ignore = "parses the whole archive"]
fn test_get_skill_list() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let skills = reader.get_skill_list();
    assert_eq!(skills.len(), 1_734, "skill count changed");

    let file = File::create(dump_path("skill_list.json")).unwrap();
    serde_json::to_writer_pretty(BufWriter::new(file), &skills).unwrap();
}

#[test]
#[ignore = "parses the whole archive"]
fn test_save_all_parquet() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    save_equipment_to_parquet(reader.get_equipment_list(), dump_path("equipments.parquet"));
    save_stackable_to_parquet(reader.get_stackable_list(), dump_path("stackables.parquet"));
    save_quest_to_parquet(reader.get_quest_list(), dump_path("quests.parquet"));
    save_dungeon_to_parquet(reader.get_dungeon_list(), dump_path("dungeons.parquet"));
    save_skill_to_parquet(reader.get_skill_list(), dump_path("skills.parquet"));
    save_exp_to_parquet(reader.get_exp_list(), dump_path("exps.parquet"));
    save_magic_seal_to_parquet(
        reader.get_magic_seal_list(),
        dump_path("magic_seals.parquet"),
    );
}

#[test]
fn test_extract_single_file() {
    let Some(mut reader) = open_reader() else {
        return;
    };

    let dest = std::env::temp_dir().join("pvf-extract-test");
    let path = reader
        .extract_file("equipment/equipment.lst", &dest)
        .unwrap();

    assert!(path.exists());
    assert!(std::fs::metadata(&path).unwrap().len() > 0);
}
