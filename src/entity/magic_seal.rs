use polars::datatypes::{DataType, Field};
use polars::prelude::Schema;
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Debug, Default)]
pub struct MagicSeal {
    pub id: u32,
    pub name: String,
}

pub fn get_magic_seal_schema() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("id".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
    ]))
}
