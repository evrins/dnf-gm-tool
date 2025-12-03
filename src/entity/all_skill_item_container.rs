use crate::entity::all_skill_item::{AllSkillItem, get_all_skill_item_dtype};
use polars::datatypes::{DataType, Field};
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct AllSkillItemContainer {
    pub all_skill_item: AllSkillItem,
}

pub fn get_all_skill_item_container_dtype() -> DataType {
    DataType::Struct(vec![Field::new(
        "all_skill_item".into(),
        get_all_skill_item_dtype(),
    )])
}
