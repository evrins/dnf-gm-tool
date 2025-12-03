use polars::prelude::{DataType, Field, Schema};
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Debug, Default)]
pub struct Skill {
    pub name: String,
    pub name2: String,
    pub job: String,
    pub basic_explain: String,
    pub explain: String,
    pub feature_skill_index: i32,
    pub skill_class: i32,
    pub id_of_job: u32,
}

pub fn get_skill_schema() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("id_of_job".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
        Field::new("name2".into(), DataType::String),
        Field::new("job".into(), DataType::String),
        Field::new("basic_explain".into(), DataType::String),
        Field::new("explain".into(), DataType::String),
        Field::new("feature_skill_index".into(), DataType::Int32),
        Field::new("skill_class".into(), DataType::Int32),
    ]))
}
