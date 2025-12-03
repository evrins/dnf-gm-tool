use crate::entity::enchant::{Enchant, get_enchant_dtype};
use crate::parser::utils::map_usable_job;
use polars::prelude::{DataType, Field, Schema};
use serde::Serialize;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Serialize, Default, Debug)]
pub struct Stackable {
    pub id: u32,
    pub name: String,
    pub name2: String,
    pub minimum_level: i32,
    pub rarity: i32,
    pub stackable_type: String,
    pub sub_stackable_type: i32,
    pub item_group_name: String,
    pub item_category: String,
    pub stack_limit: i32,
    pub usable_job: Vec<String>,
    pub enchant: Enchant,
    pub stat_desc: String,
    pub monster_card_id: i32,
    pub string_data: Vec<String>,

    pub display_rarity: String,
    pub display_stackable_type: String,
    pub display_usable_job: String,
}

impl Stackable {
    pub fn update_display_rarity(&mut self) {
        let rarity_list = ["普通", "高级", "稀有", "神器", "史诗", "勇者"];
        self.display_rarity = match rarity_list.get(self.rarity as usize) {
            Some(rarity) => rarity.to_string(),
            None => self.rarity.to_string(),
        }
    }

    pub fn update_display_stackable_type(&mut self) {
        if self.item_category == "monster card" {
            self.display_stackable_type = "卡片".to_string();
            return;
        }
        let stackable_mapping = HashMap::from([
            ("[avatar emblem]", "时装徽章"),
            ("[booster random]", "礼包"),
            ("[booster selection]", "礼包"),
            ("[booster]", "礼包"),
            ("[cera booster]", "礼包"),
            ("[cera package]", "礼包"),
            ("[usable cera package]", "礼包"),
            ("[upgrade limit cube]", "礼包"),
            ("[contract]", "契约"),
            ("[creature expitem]", "宠物经验道具"),
            ("[creature]", "宠物"),
            ("[feed]", "宠物道具"),
            ("[disguise random]", "变身道具"),
            ("[disguise]", "变身道具"),
            ("[dye]", "染色剂"),
            ("[enchant waste]", "附魔宝珠"),
            ("[expert town potion]", "秘药"),
            ("[global effect]", "频道道具"),
            ("[material expert job]", "副职业"),
            ("[material]", "材料"),
            ("[etc]", "其他"),
            ("[legacy]", "其他"),
            ("[multi upgradable legacy bonus cera]", "其他"),
            ("[multi upgradable legacy]", "其他"),
            ("[random upgradable legacy]", "其他"),
            ("[stackable legacy]", "其他"),
            ("[only effect]", "其他"),
            ("[town and dungeon]", "其他"),
            ("[unlimited town and dungeon]", "其他"),
            ("[unlimited etc]", "其他"),
            ("[upgradable legacy]", "袖珍罐"),
            ("[quest receive]", "悬赏令"),
            ("[quest]", "任务道具"),
            ("[recipe]", "设计图"),
            ("[set]", "地雷"),
            ("[teleport potion]", "瞬间移动药剂"),
            ("[throw]", "投掷物"),
            ("[waste]", "消耗品"),
            ("[unlimited waste]", "消耗品"),
        ]);

        self.display_stackable_type =
            if let Some(&d) = stackable_mapping.get(self.stackable_type.as_str()) {
                d.to_string()
            } else {
                "其他".to_string()
            }
    }

    pub fn update_display_usable_job(&mut self) {
        self.display_usable_job = map_usable_job(&self.usable_job);
    }
}

pub fn get_stackable_scheme() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("id".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
        Field::new("name2".into(), DataType::String),
        Field::new("minimum_level".into(), DataType::UInt32),
        Field::new("rarity".into(), DataType::UInt32),
        Field::new("stackable_type".into(), DataType::String),
        Field::new("sub_stackable_type".into(), DataType::UInt32),
        Field::new("item_group_name".into(), DataType::String),
        Field::new("item_category".into(), DataType::String),
        Field::new("stack_limit".into(), DataType::UInt32),
        Field::new(
            "usable_job".into(),
            DataType::List(Box::new(DataType::String)),
        ),
        Field::new("enchant".into(), get_enchant_dtype()),
        Field::new("stat_desc".into(), DataType::String),
        Field::new("monster_card_id".into(), DataType::Int32),
        Field::new("string_data".into(), DataType::List(Box::new(DataType::String))),
        Field::new("display_rarity".into(), DataType::String),
        Field::new("display_stackable_type".into(), DataType::String),
        Field::new("display_usable_job".into(), DataType::String),
    ]))
}
