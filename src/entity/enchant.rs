use crate::entity::stat_property::{StatProperty, get_stat_property_schema};
use polars::datatypes::DataType;
use polars::datatypes::Field;
use polars::prelude::SchemaExt;
use serde::Serialize;
use std::collections::HashMap;

#[derive(Serialize, Debug, Default)]
pub struct Enchant {
    #[serde(flatten)]
    pub stat_property: StatProperty,

    pub display_enchant_category: Vec<String>,
}

impl Enchant {
    pub fn sort_display_enchant_category(&mut self) {
        let keys = [
            "所有异常状态抗性",
            "回避率",
            "石化抗性",
            "束缚抗性",
            "中毒抗性",
            "减速抗性",
            "魔法防御",
            "物理防御",
            "物理暴击率",
            "魔法暴击率",
            "物理攻击力",
            "魔法攻击力",
            "力量",
            "智力",
            "体力",
            "精神",
            "独立攻击力",
            "火属性抗性",
            "光属性抗性",
            "暗属性抗性",
            "所有属性抗性",
            "火属性强化",
            "冰属性强化",
            "光属性强化",
            "暗属性强化",
            "所有属性强化",
            "攻击速度",
            "释放速度",
            "移动速度",
            "HP 回复速度",
            "MP 回复速度",
            "HP 最大值",
            "MP 最大值",
            "属性攻击",
            "跳跃力",
            "技能等级提升",
            "命中率",
            "僵直",
            "硬直",
            "特殊效果",
        ];
        let orb_category_order: HashMap<&str, usize> =
            keys.iter().enumerate().map(|(i, &v)| (v, i)).collect();

        self.display_enchant_category.sort_by_key(|k| {
            if let Some(order) = orb_category_order.get(k.as_str()) {
                *order
            } else {
                1000
            }
        });
    }
}

pub fn get_enchant_dtype() -> DataType {
    let mut fields = vec![Field::new(
        "display_enchant_category".into(),
        DataType::List(Box::new(DataType::String)),
    )];

    fields.extend(get_stat_property_schema().iter_fields().collect::<Vec<_>>());
    DataType::Struct(fields)
}
