use crate::parser::pvf_encoding::PVFEncoding;
use crate::parser::utils::to_string_with_encoding;
use byteorder::{ByteOrder, LittleEndian};
use std::collections::HashMap;

#[derive(Debug, Default)]
pub struct StringTable {
    encoding: PVFEncoding,
    cache: HashMap<usize, String>,
    _length: u32,
    buf: Vec<u8>,
}

impl StringTable {
    pub fn new(buf: Vec<u8>, encoding: PVFEncoding) -> Self {
        StringTable {
            encoding,
            _length: LittleEndian::read_u32(&buf[..4]),
            buf: buf[4..].to_vec(),
            ..Default::default()
        }
    }

    pub fn get_item(&mut self, i: u32) -> String {
        let i = i as usize;
        if let Some(s) = self.cache.get(&i) {
            s.clone()
        } else {
            let s = self._get_item(i);
            self.cache.insert(i, s.clone());
            s
        }
    }

    fn _get_item(&mut self, i: usize) -> String {
        let start = LittleEndian::read_u32(&self.buf[4 * i..4 * i + 4]) as usize;
        let end = LittleEndian::read_u32(&self.buf[4 * i + 4..4 * i + 8]) as usize;

        to_string_with_encoding(&self.buf[start..end], self.encoding)
    }
}
