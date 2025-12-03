use polars::datatypes::Field;
use polars::prelude::DataType;
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct SkillApplyCondition {
    pub skill_group: String,
    pub lower_bound_level: i32,
    pub upper_bound_level: i32,
    pub value: i32,
    pub extra_condition: Vec<String>,
}

pub fn get_skill_apply_condition() -> DataType {
    DataType::Struct(vec![
        Field::new("skill_group".into(), DataType::String),
        Field::new("lower_bound_level".into(), DataType::Int32),
        Field::new("upper_bound_level".into(), DataType::Int32),
        Field::new("value".into(), DataType::Int32),
        Field::new(
            "extra_condition".into(),
            DataType::List(Box::new(DataType::String)),
        ),
    ])
}
