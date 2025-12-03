use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct SkillLevelUp {
    pub role: String,
    pub skill_id: i32,
    pub level_up: i32,
}

pub fn get_skill_level_up_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("role".into(), DataType::String),
        Field::new("skill_id".into(), DataType::Int32),
        Field::new("level_up".into(), DataType::Int32),
    ])
}
