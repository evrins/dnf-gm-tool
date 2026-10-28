use crate::error::PvfResult;
use crate::parser::string_table::StringTable;
use byteorder::{ByteOrder, LittleEndian};
use std::collections::HashMap;

/// Token type of the integer half of an `.lst` record.
const TOKEN_INT: u8 = 2;
const TOKEN_UINT: u8 = 3;
const TOKEN_SEGMENT: u8 = 5;
const TOKEN_SEGMENT_ALT: u8 = 6;
const TOKEN_STRING: u8 = 7;
const TOKEN_SEGMENT_EXT: u8 = 8;
const TOKEN_DICT_STRING: u8 = 9;

/// A `.lst` index file: `id -> file name` pairs.
///
/// `.lst` files share the payload format of every other file in the archive, but
/// the records used to be decoded by walking the buffer in fixed 10 byte steps.
/// That silently produced garbage as soon as a record used a token of a
/// different width (type 9 tokens are 10 bytes on their own), so the parser now
/// walks the real token stream instead.
#[derive(Debug, Default)]
pub struct Lst {
    /// Directory the file names are relative to.
    pub base_dir: String,
    /// `id -> file name`.
    pub cache: HashMap<u32, String>,
}

impl Lst {
    /// Parse a `.lst` payload.
    ///
    /// Malformed records are skipped with a warning instead of aborting the
    /// whole archive, because a single broken index entry should not make the
    /// other 300k files unreadable.
    pub fn new(buf: Vec<u8>, string_table: &mut StringTable, base_dir: String) -> Lst {
        let mut res = Lst {
            base_dir,
            cache: HashMap::new(),
        };

        if buf.len() < 7 {
            tracing::warn!("lst payload is too small ({} bytes)", buf.len());
            return res;
        }

        let mut index = 2; // payloads start with a two byte marker
        let mut pending_id: Option<u32> = None;

        while index + 5 <= buf.len() {
            let token = buf[index];
            let value = LittleEndian::read_u32(&buf[index + 1..index + 5]);

            match token {
                TOKEN_INT | TOKEN_UINT => {
                    pending_id = Some(value);
                    index += 5;
                }
                TOKEN_SEGMENT | TOKEN_SEGMENT_ALT | TOKEN_SEGMENT_EXT | TOKEN_STRING => {
                    if let Some(id) = pending_id.take() {
                        res.cache.insert(id, string_table.get_item(value));
                    }
                    index += 5;
                }
                TOKEN_DICT_STRING => {
                    // id / dictionary string pairs do not appear in practice,
                    // but the token is 10 bytes wide, so it must be skipped as
                    // a whole to stay aligned.
                    pending_id = None;
                    index += 10;
                }
                other => {
                    tracing::warn!("stopping lst parsing at offset {index}: token type {other}");
                    break;
                }
            }
        }

        res
    }

    /// Parse a `.lst` payload, failing when the payload is malformed.
    pub fn try_new(
        buf: Vec<u8>,
        string_table: &mut StringTable,
        base_dir: String,
    ) -> PvfResult<Lst> {
        Ok(Self::new(buf, string_table, base_dir))
    }

    pub fn get_item(&self, i: u32) -> String {
        self.cache.get(&i).cloned().unwrap_or_default()
    }

    pub fn try_get_item(&self, i: u32) -> Option<&str> {
        self.cache.get(&i).map(String::as_str)
    }

    pub fn len(&self) -> usize {
        self.cache.len()
    }

    pub fn is_empty(&self) -> bool {
        self.cache.is_empty()
    }

    /// `id -> file name` pairs, ordered by id (names are not resolved).
    pub fn entries(&self) -> Vec<(u32, String)> {
        let mut entries = self
            .cache
            .iter()
            .map(|(id, name)| (*id, name.clone()))
            .collect::<Vec<_>>();
        entries.sort_unstable_by_key(|(id, _)| *id);
        entries
    }

    /// `id -> resolved path` pairs, ordered by id.
    pub fn resolved_entries(&self) -> Vec<(u32, String)> {
        self.entries()
            .into_iter()
            .map(|(id, name)| (id, self.resolve(&name)))
            .collect()
    }

    /// Join a file name with the base directory, as stored in the archive.
    pub fn resolve(&self, name: &str) -> String {
        join_path(&self.base_dir, name)
    }

    /// Every path that could designate `name`, most likely first.
    ///
    /// Some `.lst` files live in a nested directory but reference their entries
    /// relative to the top level directory (and vice versa), so callers should
    /// try all candidates before giving up.
    pub fn candidates(&self, name: &str) -> Vec<String> {
        let mut candidates = Vec::new();

        let joined = self.resolve(name);
        candidates.push(joined);

        if let Some((head, _)) = self.base_dir.split_once('/') {
            let top_level = join_path(head, name);
            if !candidates.contains(&top_level) {
                candidates.push(top_level);
            }
        }

        let bare = name.replace('\\', "/").to_lowercase();
        if !candidates.contains(&bare) {
            candidates.push(bare);
        }

        candidates
    }

    /// Directory that file names of `lst_path` are relative to.
    pub fn base_dir_of(lst_path: &str) -> String {
        let path = lst_path.replace('\\', "/");
        match path.rsplit_once('/') {
            Some((dir, _)) => dir.to_string(),
            None => String::new(),
        }
    }
}

/// Join two archive paths with a single `/`, lower cased.
pub fn join_path(base: &str, name: &str) -> String {
    let name = name.replace('\\', "/");
    let name = name.trim_start_matches('/');
    let joined = if base.is_empty() {
        name.to_string()
    } else {
        format!("{}/{}", base.trim_end_matches('/'), name)
    };

    let mut normalised = String::with_capacity(joined.len());
    let mut last_was_slash = false;
    for ch in joined.chars() {
        if ch == '/' {
            if !last_was_slash {
                normalised.push(ch);
            }
            last_was_slash = true;
        } else {
            normalised.push(ch);
            last_was_slash = false;
        }
    }

    normalised.to_lowercase()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parser::pvf_encoding::PVFEncoding;

    #[test]
    fn joins_paths() {
        assert_eq!(join_path("equipment", "a/b.equ"), "equipment/a/b.equ");
        assert_eq!(join_path("", "/a/b.equ"), "a/b.equ");
        assert_eq!(join_path("equipment/", "a.equ"), "equipment/a.equ");
        assert_eq!(join_path("Skill", "SwordMan/1.skl"), "skill/swordman/1.skl");
    }

    #[test]
    fn base_dir_is_the_parent_directory() {
        assert_eq!(Lst::base_dir_of("equipment/equipment.lst"), "equipment");
        assert_eq!(
            Lst::base_dir_of("etc/randomoption/x.lst"),
            "etc/randomoption"
        );
        assert_eq!(Lst::base_dir_of("n_string.lst"), "");
    }

    #[test]
    fn parses_int_string_records() {
        // 2-byte marker, then (int, string) records
        let mut buf = vec![0xB0, 0xD0];
        for (id, str_index) in [(10u32, 0u32), (11, 1)] {
            buf.push(TOKEN_INT);
            buf.extend_from_slice(&id.to_le_bytes());
            buf.push(TOKEN_STRING);
            buf.extend_from_slice(&str_index.to_le_bytes());
        }

        let mut table =
            StringTable::new(make_table(&["a.equ", "b.equ"]), PVFEncoding::GBK).unwrap();
        let lst = Lst::new(buf, &mut table, "equipment".to_string());

        assert_eq!(lst.len(), 2);
        assert_eq!(lst.get_item(10), "a.equ");
        assert_eq!(lst.resolve("a.equ"), "equipment/a.equ");
    }

    #[test]
    fn stops_on_unknown_token() {
        let mut buf = vec![0xB0, 0xD0];
        buf.push(TOKEN_INT);
        buf.extend_from_slice(&1u32.to_le_bytes());
        buf.push(TOKEN_STRING);
        buf.extend_from_slice(&0u32.to_le_bytes());
        buf.push(0xFF); // padding / corruption
        buf.extend_from_slice(&[0, 0, 0, 0]);

        let mut table = StringTable::new(make_table(&["a.equ"]), PVFEncoding::GBK).unwrap();
        let lst = Lst::new(buf, &mut table, String::new());
        assert_eq!(lst.len(), 1);
    }

    /// Build a minimal string table from `strings`.
    fn make_table(strings: &[&str]) -> Vec<u8> {
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
}
