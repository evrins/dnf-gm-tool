use polars::prelude::{DataType, Field, Schema};
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Default, Debug)]
pub struct Quest {
    pub id: u32,
    pub name: String,
    pub grade: String,
    pub difficulty: String,
    pub gold_multiple: i32,
    pub npc_index: i32,
    pub complete_npc_index: i32,
    pub job: String,
    pub grow_type: i32,
    pub level: Vec<i32>,
    pub quest_type: String,
    pub sub_type: i32,
    pub int_data: Vec<i32>,
    pub reward_type: String,
    pub depend_message: String,
    pub condition_message: String,
    pub solve_message: String,
    pub quest_point: i32,
    pub dungeon_info: Vec<i32>,
    pub relation_quest: Vec<i32>,
}

pub fn get_quest_scheme() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        Field::new("id".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
        Field::new("grade".into(), DataType::String),
        Field::new("difficulty".into(), DataType::String),
        Field::new("gold_multiple".into(), DataType::UInt32),
        Field::new("npc_index".into(), DataType::UInt32),
        Field::new("complete_npc_index".into(), DataType::UInt32),
        Field::new("job".into(), DataType::String),
        Field::new("grow_type".into(), DataType::UInt32),
        Field::new("level".into(), DataType::List(Box::new(DataType::UInt32))),
        Field::new("quest_type".into(), DataType::String),
        Field::new("sub_type".into(), DataType::UInt32),
        Field::new(
            "int_data".into(),
            DataType::List(Box::new(DataType::UInt32)),
        ),
        Field::new("reward_type".into(), DataType::String),
        Field::new("depend_message".into(), DataType::String),
        Field::new("condition_message".into(), DataType::String),
        Field::new("solve_message".into(), DataType::String),
        Field::new("quest_point".into(), DataType::UInt32),
        Field::new(
            "dungeon_info".into(),
            DataType::List(Box::new(DataType::UInt32)),
        ),
        Field::new(
            "relation_quest".into(),
            DataType::List(Box::new(DataType::UInt32)),
        ),
    ]))
}
