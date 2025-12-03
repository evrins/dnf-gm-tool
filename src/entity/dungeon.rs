use polars::datatypes::DataType;
use polars::prelude::{Field, Schema};
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Default, Debug)]
pub struct Dungeon {
    pub id: u32,
    pub name: String,
    pub explain: String,
    pub basis_level: i32,
    pub minimum_required_level: i32,
}

pub fn get_dungeon_schema() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("id".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
        Field::new("explain".into(), DataType::String),
        Field::new("basis_level".into(), DataType::Int32),
        Field::new("minimum_required_level".into(), DataType::Int32),
    ]))
}
