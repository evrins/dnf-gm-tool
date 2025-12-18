use crate::parser::string_table::StringTable;
use byteorder::{ByteOrder, LittleEndian};
use std::collections::HashMap;

#[derive(Debug, Default)]
pub struct Lst {
    pub base_dir: String,
    pub cache: HashMap<u32, String>,
}

impl Lst {
    pub fn new(buf: Vec<u8>, string_table: &mut StringTable, base_dir: String) -> Lst {
        let mut res = Lst {
            base_dir,
            cache: HashMap::new(),
        };

        let length = buf.len();

        for i in (2..length - 9).step_by(10) {
            let a = buf[i];
            let aa = LittleEndian::read_u32(&buf[i + 1..i + 5]);
            let b = buf[i + 5];
            let bb = LittleEndian::read_u32(&buf[i + 6..i + 10]);

            let mut index = 0;
            let mut string_table_index = 0;

            if a == 2 {
                index = aa;
            } else if a == 7 {
                string_table_index = aa;
            }

            if b == 2 {
                index = bb
            } else if b == 7 {
                string_table_index = bb;
            }

            let s = string_table.get_item(string_table_index);
            res.cache.insert(index, s);
        }

        res
    }

    pub fn get_item(&self, i: u32) -> String {
        self.cache.get(&i).unwrap().clone()
    }

    pub fn len(&self) -> usize {
        self.cache.len()
    }
}
