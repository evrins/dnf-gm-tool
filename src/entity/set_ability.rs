use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct SetAbility {
    pub set_name: i32,
    pub fullset_basic_explain: String,
    pub fullset_detail_explain: String,
}

pub fn get_set_ability_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("set_name".into(), DataType::Int32),
        Field::new("fullset_basic_explain".into(), DataType::String),
        Field::new("fullset_detail_explain".into(), DataType::String),
    ])
}
