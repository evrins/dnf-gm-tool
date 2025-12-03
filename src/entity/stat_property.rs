use crate::entity::all_skill_item_container::{
    AllSkillItemContainer, get_all_skill_item_container_dtype,
};
use crate::entity::item_aura::{ItemAura, get_item_aura_dtype};
use crate::entity::skill_level_up::{SkillLevelUp, get_skill_level_up_dtype};
use polars::prelude::{DataType, Field, Schema};
use serde::Serialize;
use std::sync::Arc;

#[derive(Serialize, Debug, Default)]
pub struct StatProperty {
    pub physical_attack: i32,
    pub physical_defense: i32,
    pub magical_attack: i32,
    pub magical_defense: i32,
    pub separate_attack: i32,
    pub hp_max: i32,
    pub mp_max: i32,
    pub inventory_limit: i32,
    pub hp_regen_speed: i32,
    pub hp_regen_speed_rate: i32,
    pub mp_regen_speed: i32,
    pub mp_regen_speed_rate: i32,
    pub move_speed: i32,
    pub attack_speed: i32,
    pub cast_speed: i32,
    pub stuck_resistance: i32,
    pub stuck: f32,
    pub rigidity: i32,
    pub hit_recovery: i32,
    pub all_elemental_attack: i32,
    pub all_elemental_resistance: i32,

    pub stun_resistance: i32,
    pub piercing_resistance: i32,
    pub freeze_resistance: i32,
    pub confuse_resistance: i32,
    pub poison_resistance: i32,
    pub stone_resistance: i32,
    pub blind_resistance: i32,
    pub curse_resistance: i32,
    pub bleeding_resistance: i32,
    pub lightning_resistance: i32,
    pub burn_resistance: i32,
    pub sleep_resistance: i32,
    pub slow_resistance: i32,
    pub hold_resistance: i32,

    pub dark_attack: i32,
    pub light_attack: i32,
    pub fire_attack: i32,
    pub water_attack: i32,

    pub dark_resistance: i32,
    pub light_resistance: i32,
    pub fire_resistance: i32,
    pub water_resistance: i32,

    pub all_activestatus_resistance: i32,
    pub room_list_move_speed_rate: f32,
    pub parameter_basic_explain: String,
    pub parameter_detail_explain: String,
    pub fullset_explain: String,
    pub fullset_basic_explain: String,
    pub fullset_detail_explain: String,
    pub jump_power: i32,
    pub physical_critical_hit: f32,
    pub magical_critical_hit: f32,

    pub all_skill_item_container: AllSkillItemContainer,
    pub skill_level_up: Vec<SkillLevelUp>,
    pub item_aura: Vec<ItemAura>,

    pub equipment_physical_attack: i32,
    pub equipment_magical_attack: i32,
    pub equipment_physical_defense: i32,
    pub equipment_magical_defense: i32,
    pub anti_evil: i32,

    pub flavor_text: String,
    pub explain: String,
    pub basic_explain: String,
    pub detail_explain: String,

    pub elemental_property: String,

    pub creature_magical_attack: i32,
    pub creature_physical_attack: i32,
    pub creature_skill_charge_time_rate: f32,

    pub hp_max_rate: f32,
    pub mp_max_rate: f32,

    pub lift_up: i32,

    pub string_data: Vec<String>,
}

pub fn get_stat_property_schema() -> Arc<Schema> {
    Arc::new(Schema::from_iter(vec![
        // --- Basic Integer Stats ---
        Field::new("physical_attack".into(), DataType::Int32),
        Field::new("physical_defense".into(), DataType::Int32),
        Field::new("magical_attack".into(), DataType::Int32),
        Field::new("magical_defense".into(), DataType::Int32),
        Field::new("separate_attack".into(), DataType::Int32),
        Field::new("hp_max".into(), DataType::Int32),
        Field::new("mp_max".into(), DataType::Int32),
        Field::new("inventory_limit".into(), DataType::Int32),
        Field::new("hp_regen_speed".into(), DataType::Int32),
        Field::new("hp_regen_speed_rate".into(), DataType::Int32),
        Field::new("mp_regen_speed".into(), DataType::Int32),
        Field::new("mp_regen_speed_rate".into(), DataType::Int32),
        Field::new("move_speed".into(), DataType::Int32),
        Field::new("attack_speed".into(), DataType::Int32),
        Field::new("cast_speed".into(), DataType::Int32),
        Field::new("stuck_resistance".into(), DataType::Int32),
        // --- Floats ---
        Field::new("stuck".into(), DataType::Float32),
        // --- More Ints ---
        Field::new("rigidity".into(), DataType::Int32),
        Field::new("all_elemental_attack".into(), DataType::Int32),
        Field::new("all_elemental_resistance".into(), DataType::Int32),
        // --- Resistances (Int32) ---
        Field::new("stun_resistance".into(), DataType::Int32),
        Field::new("piercing_resistance".into(), DataType::Int32),
        Field::new("freeze_resistance".into(), DataType::Int32),
        Field::new("confuse_resistance".into(), DataType::Int32),
        Field::new("poison_resistance".into(), DataType::Int32),
        Field::new("stone_resistance".into(), DataType::Int32),
        Field::new("blind_resistance".into(), DataType::Int32),
        Field::new("curse_resistance".into(), DataType::Int32),
        Field::new("bleeding_resistance".into(), DataType::Int32),
        Field::new("lightning_resistance".into(), DataType::Int32),
        Field::new("burn_resistance".into(), DataType::Int32),
        Field::new("sleep_resistance".into(), DataType::Int32),
        Field::new("slow_resistance".into(), DataType::Int32),
        Field::new("hold_resistance".into(), DataType::Int32),
        // --- Elemental Attacks (Int32) ---
        Field::new("dark_attack".into(), DataType::Int32),
        Field::new("light_attack".into(), DataType::Int32),
        Field::new("fire_attack".into(), DataType::Int32),
        Field::new("water_attack".into(), DataType::Int32),
        // --- Elemental Resistances (Int32) ---
        Field::new("dark_resistance".into(), DataType::Int32),
        Field::new("light_resistance".into(), DataType::Int32),
        Field::new("fire_resistance".into(), DataType::Int32),
        Field::new("water_resistance".into(), DataType::Int32),
        Field::new("all_activestatus_resistance".into(), DataType::Int32),
        // --- Float ---
        Field::new("room_list_move_speed_rate".into(), DataType::Float32),
        // --- Strings ---
        Field::new("parameter_basic_explain".into(), DataType::String),
        Field::new("parameter_detail_explain".into(), DataType::String),
        Field::new("fullset_explain".into(), DataType::String),
        Field::new("fullset_basic_explain".into(), DataType::String),
        Field::new("fullset_detail_explain".into(), DataType::String),
        // --- Mixed Stats ---
        Field::new("jump_power".into(), DataType::Int32),
        Field::new("physical_critical_hit".into(), DataType::Float32),
        Field::new("magical_critical_hit".into(), DataType::Float32),
        // --- Complex Nested Types (Vec<Struct>) ---
        // Maps to List(Struct(...))
        Field::new(
            "all_skill_item_container".into(),
            get_all_skill_item_container_dtype(),
        ),
        Field::new(
            "skill_level_up".into(),
            DataType::List(Box::new(get_skill_level_up_dtype())),
        ),
        Field::new(
            "item_aura".into(),
            DataType::List(Box::new(get_item_aura_dtype())),
        ),
        // --- Equipment Stats ---
        Field::new("equipment_physical_attack".into(), DataType::Int32),
        Field::new("equipment_magical_attack".into(), DataType::Int32),
        Field::new("equipment_physical_defense".into(), DataType::Int32),
        Field::new("equipment_magical_defense".into(), DataType::Int32),
        Field::new("anti_evil".into(), DataType::Int32),
        Field::new("hit_recovery".into(), DataType::Int32),
        // --- Explanations (Strings) ---
        Field::new("flavor_text".into(), DataType::String),
        Field::new("explain".into(), DataType::String),
        Field::new("basic_explain".into(), DataType::String),
        Field::new("detail_explain".into(), DataType::String),
        Field::new("elemental_property".into(), DataType::String),
        // --- Creature Stats ---
        Field::new("creature_magical_attack".into(), DataType::Int32),
        Field::new("creature_physical_attack".into(), DataType::Int32),
        Field::new("creature_skill_charge_time_rate".into(), DataType::Float32),
        Field::new("hp_max_rate".into(), DataType::Float32),
        Field::new("mp_max_rate".into(), DataType::Float32),
        Field::new("lift_up".into(), DataType::Int32),
        Field::new(
            "string_data".into(),
            DataType::List(Box::new(DataType::String)),
        ),
    ]))
}
