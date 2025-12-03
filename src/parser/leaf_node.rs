use serde::Serialize;

#[derive(Serialize, Debug, Clone)]
pub struct LeafNode {
    pub file_number: u32,
    pub file_path: String,
    pub file_length: u32,
    pub file_crc32: u32,
    pub relative_offset: u64,
}

impl LeafNode {
    pub fn new() -> Self {
        Self {
            file_number: 0,
            file_path: "".to_string(),
            file_length: 0,
            file_crc32: 0,
            relative_offset: 0,
        }
    }
}
