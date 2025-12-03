use crate::parser::leaf_node::LeafNode;
use std::collections::HashMap;

#[derive(Debug)]
pub struct PVFHeader {
    pub uuid: String,
    pub version: u32,
    pub leaf_map: HashMap<String, LeafNode>,
    pub header_length: u64,
    pub dir_tree_length: u32,
    pub file_pack_index_shift: u64,
}

impl PVFHeader {
    pub fn new() -> Self {
        Self {
            uuid: String::new(),
            version: 0,
            leaf_map: Default::default(),
            header_length: 0,
            dir_tree_length: 0,
            file_pack_index_shift: 0,
        }
    }
}
