use polars::datatypes::{DataType, Field};
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct ItemAura {
    pub aura_type: String,
    pub op: String,
    pub num: i32,
    pub distance: i32,
}

pub fn get_item_aura_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("aura_type".into(), DataType::String),
        Field::new("op".into(), DataType::String),
        Field::new("num".into(), DataType::Int32),
        Field::new("distance".into(), DataType::Int32),
    ])
}
