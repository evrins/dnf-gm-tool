use crate::parser::pvf_encoding::PVFEncoding;
use crate::parser::utils::to_string_with_encoding;
use std::collections::HashMap;

#[derive(Debug)]
pub struct Str {
    cache: HashMap<String, String>,
}

impl Str {
    pub fn new(buf: &[u8], encoding: PVFEncoding) -> Str {
        let s = to_string_with_encoding(buf, encoding);
        let mut cache: HashMap<String, String> = HashMap::new();

        for line in s.split('\n') {
            if !line.contains('>') {
                continue;
            }
            let mut rs = line.splitn(2, '>');
            let key = rs.next().unwrap().to_string();
            let val = rs.next().unwrap().to_string();
            cache.insert(key, val);
        }

        Str { cache }
    }

    pub fn get_item(&self, key: &str) -> String {
        match self.cache.get(key) {
            Some(val) => val.replace("\r", "").clone(),
            None => "None".to_string(),
        }
    }
}
