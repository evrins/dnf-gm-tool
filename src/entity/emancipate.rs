use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct Emancipate {
    pub input: Vec<i32>,
    pub output: Vec<i32>,
    pub emancipate_explain: String,
}

pub fn get_emancipate_dtype() -> DataType {
    DataType::Struct(vec![
        Field::new("input".into(), DataType::List(Box::new(DataType::Int32))),
        Field::new("output".into(), DataType::List(Box::new(DataType::Int32))),
        Field::new("emancipate_explain".into(), DataType::String),
    ])
}
