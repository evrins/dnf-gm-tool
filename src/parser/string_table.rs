use crate::error::{PvfError, PvfResult};
use crate::parser::pvf_encoding::PVFEncoding;
use crate::parser::utils::to_string_with_encoding;
use byteorder::{ByteOrder, LittleEndian};
use std::collections::HashMap;

/// The shared string table (`stringtable.bin`).
///
/// Layout:
///
/// ```text
/// u32    string_count
/// u32[]  offsets      (string_count + 1 entries, relative to the offsets array)
/// u8[]   data         (concatenated strings, no terminators)
/// ```
///
/// Every token of type 5/6/7/8 in a payload is an index into this table, so it
/// is the single most used structure of the whole archive.
#[derive(Debug, Default)]
pub struct StringTable {
    encoding: PVFEncoding,
    cache: HashMap<u32, String>,
    count: u32,
    /// Offsets + data, i.e. the file without its leading `string_count`.
    buf: Vec<u8>,
}

impl StringTable {
    pub fn new(buf: Vec<u8>, encoding: PVFEncoding) -> PvfResult<Self> {
        if buf.len() < 8 {
            return Err(PvfError::format(format!(
                "string table is too small ({} bytes)",
                buf.len()
            )));
        }

        let count = LittleEndian::read_u32(&buf[..4]);
        // Offsets are relative to the offsets array itself, not to the file start.
        let offsets_len = buf.len() - 4;
        if count == 0 || 4 * (count as usize + 1) > offsets_len {
            return Err(PvfError::format(format!(
                "string table declares {count} strings but only holds {offsets_len} bytes"
            )));
        }

        Ok(Self {
            encoding,
            cache: HashMap::new(),
            count,
            buf: buf[4..].to_vec(),
        })
    }

    pub fn len(&self) -> u32 {
        self.count
    }

    pub fn is_empty(&self) -> bool {
        self.count == 0
    }

    pub fn encoding(&self) -> PVFEncoding {
        self.encoding
    }

    /// Byte range of the raw string `index` inside the data area.
    fn bounds(&self, index: u32) -> PvfResult<(usize, usize)> {
        if index >= self.count {
            return Err(PvfError::StringTable {
                index,
                count: self.count,
            });
        }

        let i = index as usize;
        let start = LittleEndian::read_u32(&self.buf[4 * i..4 * i + 4]) as usize;
        let end = LittleEndian::read_u32(&self.buf[4 * i + 4..4 * i + 8]) as usize;

        if end < start || end > self.buf.len() {
            return Err(PvfError::format(format!(
                "string {index} points outside the table: [{start}, {end})"
            )));
        }

        Ok((start, end))
    }

    /// The undecoded bytes of `index`.
    pub fn raw(&self, index: u32) -> PvfResult<&[u8]> {
        let (start, end) = self.bounds(index)?;
        Ok(&self.buf[start..end])
    }

    /// The decoded string of `index`.
    pub fn try_get_item(&mut self, index: u32) -> PvfResult<String> {
        if let Some(value) = self.cache.get(&index) {
            return Ok(value.clone());
        }

        let (start, end) = self.bounds(index)?;
        let value = to_string_with_encoding(&self.buf[start..end], self.encoding);
        self.cache.insert(index, value.clone());
        Ok(value)
    }

    /// The decoded string of `index`, or an empty string when the reference is
    /// broken.  Kept for callers that cannot propagate an error.
    pub fn get_item(&mut self, index: u32) -> String {
        match self.try_get_item(index) {
            Ok(value) => value,
            Err(err) => {
                tracing::warn!("{err}");
                String::new()
            }
        }
    }

    /// Find every string containing `needle` (case insensitive).
    pub fn search(&mut self, needle: &str, limit: Option<usize>) -> Vec<(u32, String)> {
        let needle = needle.to_lowercase();
        let mut found = Vec::new();

        for index in 0..self.count {
            let value = self.get_item(index);
            if value.to_lowercase().contains(&needle) {
                found.push((index, value));
                if limit.is_some_and(|limit| found.len() >= limit) {
                    break;
                }
            }
        }

        found
    }

    pub fn clear_cache(&mut self) {
        self.cache.clear();
    }
}
