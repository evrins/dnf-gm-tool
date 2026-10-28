use crate::error::{PvfError, PvfResult};
use byteorder::{ByteOrder, LittleEndian};
use serde::Serialize;
use std::collections::HashMap;

/// Longest path accepted in the directory tree; guards against a corrupted
/// length field turning into a multi-gigabyte allocation.
const MAX_PATH_LENGTH: u32 = 4096;

/// One entry of the directory tree.
#[derive(Serialize, Debug, Clone, Default)]
pub struct LeafNode {
    pub file_number: u32,
    pub file_path: String,
    /// Length of the payload as stored in the header.
    pub file_length: u32,
    /// Doubles as the decryption key of the payload.
    pub file_crc32: u32,
    pub relative_offset: u64,
}

impl LeafNode {
    pub fn new() -> Self {
        Self::default()
    }

    /// Length actually occupied in the archive: payloads are padded to 4 bytes.
    pub fn padded_length(&self) -> u32 {
        (self.file_length + 3) & !3
    }

    /// Lower case file extension without the dot.
    pub fn suffix(&self) -> &str {
        match self.file_path.rsplit_once('.') {
            Some((_, suffix)) => suffix,
            None => "",
        }
    }

    pub fn directory(&self) -> &str {
        match self.file_path.rsplit_once('/') {
            Some((dir, _)) => dir,
            None => "",
        }
    }
}

/// Parse one leaf record, returning it and the offset right after it.
pub fn parse_leaf(buf: &[u8], index: usize) -> PvfResult<(LeafNode, usize)> {
    if index + 8 > buf.len() {
        return Err(PvfError::Truncated {
            what: "leaf record",
            expected: index + 8,
            actual: buf.len(),
        });
    }

    let mut res = LeafNode::new();
    res.file_number = LittleEndian::read_u32(&buf[index..index + 4]);
    let file_path_length = LittleEndian::read_u32(&buf[index + 4..index + 8]) as usize;
    let mut index = index + 8;

    if file_path_length > MAX_PATH_LENGTH as usize || index + file_path_length + 12 > buf.len() {
        return Err(PvfError::format(format!(
            "invalid path length {file_path_length} at offset {index}"
        )));
    }

    // Paths are ascii and already lower case in every known client, but be
    // tolerant: a non-ascii byte must not abort the whole archive.
    res.file_path = String::from_utf8_lossy(&buf[index..index + file_path_length]).to_string();
    index += file_path_length;

    res.file_length = LittleEndian::read_u32(&buf[index..index + 4]);
    res.file_crc32 = LittleEndian::read_u32(&buf[index + 4..index + 8]);
    res.relative_offset = LittleEndian::read_u32(&buf[index + 8..index + 12]) as u64;

    Ok((res, index + 12))
}

/// Parse the whole (already decrypted) directory tree.
pub fn parse_leafs(buf: &[u8], num_files_in_dir_tree: u32) -> PvfResult<HashMap<String, LeafNode>> {
    let mut leaf_map: HashMap<String, LeafNode> =
        HashMap::with_capacity(num_files_in_dir_tree as usize);
    let mut index = 0;

    for _ in 0..num_files_in_dir_tree {
        let (leaf_node, new_index) = parse_leaf(buf, index)?;
        index = new_index;
        leaf_map.insert(leaf_node.file_path.clone(), leaf_node);
    }

    Ok(leaf_map)
}
