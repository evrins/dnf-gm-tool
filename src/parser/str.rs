use crate::parser::pvf_encoding::PVFEncoding;
use crate::parser::utils::to_string_auto;
use std::collections::HashMap;

/// A `*.str` dictionary: `key>value` lines, referenced by token type 9.
#[derive(Debug, Default)]
pub struct Str {
    cache: HashMap<String, String>,
}

impl Str {
    /// Parse a dictionary payload.
    ///
    /// The declared archive encoding is only a hint: a BIG5 archive can ship
    /// GBK dictionaries, so the payload is decoded with detection.
    pub fn new(buf: &[u8], encoding: PVFEncoding) -> Str {
        let text = to_string_auto(buf, encoding);
        let mut cache: HashMap<String, String> = HashMap::new();

        for line in text.split('\n') {
            let Some((key, value)) = line.split_once('>') else {
                continue;
            };
            cache.insert(
                key.trim().to_string(),
                value.trim_end_matches('\r').to_string(),
            );
        }

        Str { cache }
    }

    /// Look a key up, returning `None` when the dictionary has no such entry.
    pub fn get(&self, key: &str) -> Option<String> {
        self.cache.get(key).cloned()
    }
}
