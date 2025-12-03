use crate::entity::skill_apply_condition::{SkillApplyCondition, get_skill_apply_condition};
use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct AllSkillItem {
    pub item_grow_type: String,
    pub skill_phase: String,
    pub skill_apply_condition: SkillApplyCondition,
}

pub fn get_all_skill_item_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("item_grow_type".into(), DataType::String),
        Field::new("skill_phase".into(), DataType::String),
        Field::new("skill_apply_condition".into(), get_skill_apply_condition()),
    ])
}
