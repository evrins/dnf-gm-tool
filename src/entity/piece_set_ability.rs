use crate::entity::stat_property::{StatProperty, get_stat_property_schema};
use polars::datatypes::Field;
use polars::prelude::{DataType, SchemaExt};
use serde::Serialize;

#[derive(Serialize, Default, Debug)]
pub struct PieceSetAbility {
    pub part_count: i32,

    #[serde(flatten)]
    pub stat_property: StatProperty,
}

pub fn get_piece_set_ability_dtype() -> DataType {
    let mut fields = vec![Field::new("part_count".into(), DataType::Int32)];
    fields.extend(get_stat_property_schema().iter_fields().collect::<Vec<_>>());

    DataType::Struct(fields)
}
