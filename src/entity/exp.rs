use polars::datatypes::{DataType, Field};
use polars::prelude::Schema;
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Debug, Default)]
pub struct Exp {
    pub level: i32,
    pub exp: i32,
}

pub fn get_exp_schema() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("level".into(), DataType::Int32),
        Field::new("exp".into(), DataType::Int32),
    ]))
}
