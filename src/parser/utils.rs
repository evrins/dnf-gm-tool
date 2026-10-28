use crate::parser::pvf_encoding::PVFEncoding;
use encoding_rs::{BIG5, GBK};
use std::collections::HashMap;
use zhconv::{Variant, zhconv};

pub fn map_usable_job(usable_job: &[String]) -> String {
    let job_name_mapping = HashMap::from([
        ("[all]", "全部职业"),
        ("[swordman]", "鬼剑士"),
        ("[fighter]", "格斗家"),
        ("[at fighter]", "格斗家-男"),
        ("[gunner]", "神枪手"),
        ("[at gunner]", "神枪手-女"),
        ("[mage]", "魔法师"),
        ("[at mage]", "魔法师-男"),
        ("[priest]", "圣职者"),
        ("[thief]", "暗夜使者"),
        ("[demonic swordman]", "黑暗武士"),
        ("[creator mage]", "缔造者"),
        ("[smiest]", "圣职者-女"),
    ]);

    let tmp: Vec<String> = usable_job
        .iter()
        .map(|it| {
            job_name_mapping
                .get(it.as_str())
                .cloned()
                .unwrap_or(it.as_str())
                .to_string()
        })
        .collect();

    tmp.join(",")
}

/// Decode `buf` with the given encoding.
///
/// ASCII (which is the vast majority of the string table: tag names and value
/// keys) takes a fast path that skips both the decoder and the traditional to
/// simplified conversion.
pub fn to_string_with_encoding(buf: &[u8], encoding: PVFEncoding) -> String {
    if buf.is_ascii() {
        return String::from_utf8_lossy(buf).to_string();
    }
    decode_raw(buf, encoding).0
}

/// Decode `buf`, falling back to the other legacy encoding when the preferred
/// one produces invalid sequences.
///
/// Archives are not consistent: a "GBK" archive regularly ships BIG5 `*.str`
/// dictionaries (and vice versa), so payloads that are not part of the string
/// table must be decoded with detection instead of the declared encoding.
pub fn to_string_auto(buf: &[u8], preferred: PVFEncoding) -> String {
    if buf.is_ascii() {
        return String::from_utf8_lossy(buf).to_string();
    }

    // hand edited files are sometimes plain utf-8
    if let Ok(text) = std::str::from_utf8(buf) {
        return text.to_string();
    }

    let (text, had_errors) = decode_raw(buf, preferred);
    if !had_errors {
        return text;
    }

    let fallback = preferred.other();
    let (fallback_text, fallback_errors) = decode_raw(buf, fallback);
    if fallback_errors { text } else { fallback_text }
}

/// Guess the encoding of an archive from a few payloads.
///
/// Both legacy encodings accept most byte pairs, so the score is dominated by
/// the sequences that are *invalid* for a codec (BIG5 rejects lead bytes below
/// `0xA1`, which is exactly what GBK text is full of).  Ties go to GBK, which is
/// the common case for the archives this tool targets.
pub fn guess_encoding(samples: &[Vec<u8>]) -> PVFEncoding {
    let mut gbk = 0i64;
    let mut big5 = 0i64;

    for buf in samples {
        gbk += encoding_score(buf, PVFEncoding::GBK);
        big5 += encoding_score(buf, PVFEncoding::BIG5);
    }

    if big5 > gbk {
        PVFEncoding::BIG5
    } else {
        PVFEncoding::GBK
    }
}

fn encoding_score(buf: &[u8], encoding: PVFEncoding) -> i64 {
    let (text, had_errors) = decode_raw(buf, encoding);
    let replacements = text.matches('\u{FFFD}').count() as i64;
    let cjk = text
        .chars()
        .filter(|ch| ('\u{4e00}'..='\u{9fff}').contains(ch))
        .count() as i64;

    cjk - replacements * 8 - i64::from(had_errors) * 32
}

/// Decode and report whether the bytes were valid for the encoding.
fn decode_raw(buf: &[u8], encoding: PVFEncoding) -> (String, bool) {
    match encoding {
        PVFEncoding::GBK => {
            let (s, _, had_errors) = GBK.decode(buf);
            (s.to_string(), had_errors)
        }
        PVFEncoding::BIG5 => {
            let (s, _, had_errors) = BIG5.decode(buf);
            (zhconv(s.to_string().as_str(), Variant::ZhCN), had_errors)
        }
    }
}
