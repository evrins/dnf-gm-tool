use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct AvatarSelectAbility {
    pub ability_type: String,
    pub role: String,
    pub skill_id: i32,
    pub level_up: i32,
}

pub fn get_avatar_select_ability_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("ability_type".into(), DataType::String),
        Field::new("role".into(), DataType::String),
        Field::new("skill_id".into(), DataType::Int32),
        Field::new("level_up".into(), DataType::Int32),
    ])
}
