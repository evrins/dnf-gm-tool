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

pub fn to_string_with_encoding(buf: &[u8], encoding: PVFEncoding) -> String {
    match encoding {
        PVFEncoding::GBK => {
            let (s, _, _) = GBK.decode(buf);
            s.to_string()
        }
        PVFEncoding::BIG5 => {
            let (s, _, _) = BIG5.decode(buf);
            zhconv(s.to_string().as_str(), Variant::ZhCN)
        }
    }
}
