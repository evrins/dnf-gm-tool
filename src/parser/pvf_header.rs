use crate::error::{PvfError, PvfResult};
use crate::parser::leaf_node::{LeafNode, parse_leafs};
use crate::parser::pvf_reader::decrypt_bytes;
use byteorder::{LittleEndian, ReadBytesExt};
use std::collections::HashMap;
use std::io::Read;

/// A uuid longer than this is a sure sign of a corrupted header.
const MAX_UUID_LENGTH: u32 = 4096;

/// Header of a Script.pvf archive.
///
/// Layout (all integers little endian):
///
/// ```text
/// u32   uuid_length
/// u8[]  uuid                  (ascii, uuid_length bytes)
/// u32   version
/// u32   dir_tree_length
/// u32   dir_tree_crc32        (also the decryption key of the tree)
/// u32   file_count
/// u8[]  dir_tree              (dir_tree_length bytes, encrypted)
/// ```
#[derive(Debug, Default)]
pub struct PVFHeader {
    pub uuid: String,
    pub version: u32,
    pub leaf_map: HashMap<String, LeafNode>,
    /// Offset of the first byte after the header (i.e. of the directory tree).
    pub header_length: u64,
    pub dir_tree_length: u32,
    /// Absolute offset of the packed file area.
    pub file_pack_index_shift: u64,
}

impl PVFHeader {
    pub fn new() -> Self {
        Self::default()
    }

    /// Read, decrypt and parse the header.  The reader is left positioned at the
    /// beginning of the packed file area.
    pub fn read<R: Read>(reader: &mut R) -> PvfResult<Self> {
        let uuid_len = read_u32(reader, "uuid length")?;
        if uuid_len == 0 || uuid_len > MAX_UUID_LENGTH {
            return Err(PvfError::format(format!(
                "implausible uuid length: {uuid_len}"
            )));
        }

        let mut uuid_buf = vec![0u8; uuid_len as usize];
        read_exact(reader, &mut uuid_buf, "uuid")?;

        let version = read_u32(reader, "version")?;
        let dir_tree_length = read_u32(reader, "directory tree length")?;
        let dir_tree_crc32 = read_u32(reader, "directory tree crc")?;
        let file_count = read_u32(reader, "file count")?;

        let header_length = 4 + uuid_len as u64 + 4 + 12;

        if dir_tree_length == 0 || dir_tree_length % 4 != 0 {
            return Err(PvfError::format(format!(
                "implausible directory tree length: {dir_tree_length}"
            )));
        }
        // every leaf record is at least 8 + 1 + 12 bytes
        if file_count as u64 > dir_tree_length as u64 / 20 {
            return Err(PvfError::format(format!(
                "implausible file count {file_count} for a {dir_tree_length} byte tree"
            )));
        }

        let mut tree = vec![0u8; dir_tree_length as usize];
        read_exact(reader, &mut tree, "directory tree")?;
        let tree = decrypt_bytes(tree, dir_tree_crc32);

        Ok(Self {
            uuid: String::from_utf8_lossy(&uuid_buf).to_string(),
            version,
            leaf_map: parse_leafs(&tree, file_count)?,
            header_length,
            dir_tree_length,
            file_pack_index_shift: header_length + dir_tree_length as u64,
        })
    }

    pub fn file_count(&self) -> usize {
        self.leaf_map.len()
    }

    pub fn contains(&self, file_path: &str) -> bool {
        self.leaf_map.contains_key(&normalize_path(file_path))
    }

    pub fn get(&self, file_path: &str) -> Option<&LeafNode> {
        self.leaf_map.get(&normalize_path(file_path))
    }

    /// Every directory present in the archive, sorted.
    pub fn directories(&self) -> Vec<String> {
        let mut dirs = self
            .leaf_map
            .values()
            .filter(|leaf| !leaf.directory().is_empty())
            .map(|leaf| leaf.directory().to_string())
            .collect::<Vec<_>>();
        dirs.sort_unstable();
        dirs.dedup();
        dirs
    }
}

/// Normalise an archive path: lower case, `/` separators, no empty segments.
pub fn normalize_path(path: &str) -> String {
    let path = path.trim().replace('\\', "/");
    let mut out = String::with_capacity(path.len());
    let mut last_was_slash = true; // swallow leading slashes

    for ch in path.chars() {
        if ch == '/' {
            if !last_was_slash {
                out.push(ch);
            }
            last_was_slash = true;
        } else {
            out.push(ch);
            last_was_slash = false;
        }
    }

    out.trim_end_matches('/').to_lowercase()
}

fn read_u32<R: Read>(reader: &mut R, what: &'static str) -> PvfResult<u32> {
    reader.read_u32::<LittleEndian>().map_err(|err| {
        if err.kind() == std::io::ErrorKind::UnexpectedEof {
            PvfError::Truncated {
                what,
                expected: 4,
                actual: 0,
            }
        } else {
            PvfError::Io(err)
        }
    })
}

fn read_exact<R: Read>(reader: &mut R, buf: &mut [u8], what: &'static str) -> PvfResult<()> {
    reader.read_exact(buf).map_err(|err| {
        if err.kind() == std::io::ErrorKind::UnexpectedEof {
            PvfError::Truncated {
                what,
                expected: buf.len(),
                actual: 0,
            }
        } else {
            PvfError::Io(err)
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normalizes_paths() {
        assert_eq!(normalize_path("Equipment/A.EQU"), "equipment/a.equ");
        assert_eq!(normalize_path("//a//b\\c.txt"), "a/b/c.txt");
        assert_eq!(normalize_path("a/b/"), "a/b");
    }

    #[test]
    fn rejects_garbage_header() {
        let mut cursor = std::io::Cursor::new(vec![0u8; 4]);
        let err = PVFHeader::read(&mut cursor).unwrap_err();
        assert!(matches!(err, PvfError::Format(_)), "{err}");
    }

    #[test]
    fn rejects_truncated_header() {
        let mut cursor = std::io::Cursor::new(b"ab".to_vec());
        let err = PVFHeader::read(&mut cursor).unwrap_err();
        assert!(matches!(err, PvfError::Truncated { .. }), "{err}");
    }
}
