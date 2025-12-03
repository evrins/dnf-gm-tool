use crate::entity::all_skill_item::{AllSkillItem, get_all_skill_item_dtype};
use crate::entity::avatar_select_ability::{AvatarSelectAbility, get_avatar_select_ability_dtype};
use crate::entity::emancipate::{Emancipate, get_emancipate_dtype};
use crate::entity::piece_set_ability::{PieceSetAbility, get_piece_set_ability_dtype};
use crate::entity::set_ability::{SetAbility, get_set_ability_dtype};
use crate::entity::stat_property::{StatProperty, get_stat_property_schema};
use crate::parser::utils::map_usable_job;
use polars::prelude::{DataType, Field, Schema, SchemaExt};
use serde::Serialize;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Serialize, Default, Debug)]
pub struct Equipment {
    #[serde(flatten)]
    pub stat_property: StatProperty,

    pub id: u32,
    pub name: String,
    pub name2: String,
    pub grade: i32,
    pub rarity: i32,
    pub usable_job: Vec<String>,
    pub minimum_level: i32,
    pub maximum_level: i32,
    pub price: i32,
    pub repair_price: i32,
    pub value: i32,
    pub equipment_type: String,
    pub sub_type: i32,
    pub durability: i32,
    pub weight: i32,
    pub item_group_name: String,
    pub cool_time: i32,
    pub set_name: String,
    pub set_item: Vec<i32>,
    pub enable_dye: Vec<i32>,
    pub part_set_index: i32,
    pub avatar_select_ability: Vec<AvatarSelectAbility>,
    pub item_category: String,
    pub set_ability: SetAbility,
    pub set_item_master: i32,
    pub all_skill_item: Vec<AllSkillItem>,
    pub push_aside: i32,

    // creature start
    pub int_data: Vec<i32>,
    pub creature_species: i32,
    pub output_index: i32,
    pub cash: i32,
    pub creature_min_level: i32,
    pub creature_skill_consume_mp_rate: f32,
    pub creature_skill_over_charge_time_rate: f32,
    pub creature_experience_amount_rate: f32,
    pub creature_physical_critical_hit: f32,
    pub creature_magical_critical_hit: f32,
    pub creature_stuck: f32,

    // 远古装备
    pub emancipate: Emancipate,

    // 决斗装备
    pub minimum_rank: i32,
    pub usable_world: Vec<String>,

    // 副职业
    pub prof_compound_rate: i32,
    pub prof_additional_gain_exp: Vec<i32>,
    pub prof_result_variation: Vec<i32>,
    pub prof_disjoint_result_variation: Vec<i32>,
    pub prof_material_variation: Vec<i32>,

    // 光环
    pub aurora_avatar: i32,

    // 时装
    pub clear_avatar: i32,

    pub special_monster_drop: i32,
    pub difficulty_for_extra_drop: Vec<String>,
    pub dungeon_type_for_extra_drop: Vec<String>,

    pub piece_set_ability: Vec<PieceSetAbility>,

    // field for display
    pub armor_type: String,
    pub display_equipment_type: String,
    pub display_rarity: String,
    pub display_usable_job: String,
}

impl Equipment {
    pub fn update_armor_type(&mut self) {
        if self.item_group_name == "" {
            return;
        }

        match self.equipment_type.as_str() {
            "[coat]" | "[waist]" | "[shoulder]" | "[pants]" | "[shoes]" => {
                self.armor_type = self.item_group_name.split(" ").next().unwrap().to_string();
            }
            _ => {
                return;
            }
        }
    }

    pub fn update_display_equipment_type(&mut self) {
        let weapon_mapping = HashMap::from([
            ("ssword", "短剑"),
            ("katana", "太刀"),
            ("lswd", "巨剑"),
            ("club", "钝器"),
            ("beamswd", "光剑"),
            ("knuckle", "手套"),
            ("gauntlet", "臂铠"),
            ("claw", "爪"),
            ("bglove", "拳套"),
            ("tonfa", "东方棍"),
            ("automatic", "自动手枪"),
            ("bowgun", "手弩"),
            ("revolver", "左轮"),
            ("musket", "步枪"),
            ("hcannon", "手炮"),
            ("staff", "法杖"),
            ("rod", "魔杖"),
            ("pole", "棍棒"),
            ("spear", "矛"),
            ("broom", "扫把"),
            ("cross", "十字架"),
            ("scythe", "镰刀"),
            ("rosary", "念珠"),
            ("totem", "图腾"),
            ("axe", "战斧"),
            ("wand", "手杖"),
            ("dagger", "匕首"),
            ("twinswd", "双剑"),
        ]);

        let equipment_mapping = HashMap::from([
            ("", "契约效果"),
            ("[artifact blue]", "蓝色 宠物装备"),
            ("[artifact green]", "绿色 宠物装备"),
            ("[artifact red]", "红色 宠物装备"),
            ("[aurora avatar]", "光环"),
            ("[hair avatar]", "头部装扮"),
            ("[hat avatar]", "帽子装扮"),
            ("[face avatar]", "脸部装扮"),
            ("[breast avatar]", "胸部装扮"),
            ("[coat avatar]", "上衣装扮"),
            ("[skin avatar]", "皮肤装扮"),
            ("[waist avatar]", "腰部装扮"),
            ("[pants avatar]", "下装装扮"),
            ("[shoes avatar]", "脚部装扮"),
            ("[coat]", "上衣"),
            ("[waist]", "腰带"),
            ("[pants]", "下装"),
            ("[shoulder]", "头肩"),
            ("[shoes]", "鞋子"),
            ("[magic stone]", "魔法石"),
            ("[support]", "辅助装备"),
            ("[creature]", "宠物"),
            ("[title name]", "称号"),
            ("[weapon]", "武器"),
            ("[wrist]", "手镯"),
            ("[amulet]", "项链"),
            ("[ring]", "戒指"),
        ]);

        self.display_equipment_type = if self.equipment_type == "[weapon]" {
            weapon_mapping
                .get(self.item_group_name.as_str())
                .cloned()
                .unwrap_or(self.item_group_name.as_str())
                .to_string()
        } else {
            equipment_mapping
                .get(self.equipment_type.as_str())
                .cloned()
                .unwrap_or(self.equipment_type.as_str())
                .to_string()
        }
    }

    pub fn update_display_rarity(&mut self) {
        if self.name.starts_with("传承") {
            self.display_rarity = "传承".into();
            return;
        }

        if self.item_category.contains("boss drop") {
            self.display_rarity = "领主神器".into();
            return;
        }

        self.display_rarity = match self.rarity {
            0 => "普通".into(),
            1 => "高级".into(),
            2 => "稀有".into(),
            3 => "神器".into(),
            4 => "史诗".into(),
            5 => "勇者".into(),
            _ => self.rarity.to_string().into(),
        };
    }

    pub fn update_display_usable_job(&mut self) {
        self.display_usable_job = map_usable_job(&self.usable_job);
    }
}

pub fn get_equipment_schema() -> Arc<Schema> {
    let mut s = Schema::from_iter(vec![
        Field::new("id".into(), DataType::UInt32),
        Field::new("grade".into(), DataType::Int32),
        Field::new("rarity".into(), DataType::Int32),
        Field::new("minimum_level".into(), DataType::Int32),
        Field::new("maximum_level".into(), DataType::Int32),
        Field::new("price".into(), DataType::Int32),
        Field::new("repair_price".into(), DataType::Int32),
        Field::new("value".into(), DataType::Int32),
        Field::new("sub_type".into(), DataType::Int32),
        Field::new("durability".into(), DataType::Int32),
        Field::new("weight".into(), DataType::Int32),
        Field::new("cool_time".into(), DataType::Int32),
        Field::new("part_set_index".into(), DataType::Int32),
        Field::new("set_item_master".into(), DataType::Int32),
        Field::new("push_aside".into(), DataType::Int32),
        Field::new("creature_species".into(), DataType::Int32),
        Field::new("output_index".into(), DataType::Int32),
        Field::new("cash".into(), DataType::Int32),
        Field::new("creature_min_level".into(), DataType::Int32),
        Field::new("minimum_rank".into(), DataType::Int32),
        Field::new("prof_compound_rate".into(), DataType::Int32),
        Field::new("aurora_avatar".into(), DataType::Int32),
        Field::new("clear_avatar".into(), DataType::Int32),
        Field::new("special_monster_drop".into(), DataType::Int32),
        // --- Floats (f32) ---
        Field::new("creature_skill_consume_mp_rate".into(), DataType::Float32),
        Field::new(
            "creature_skill_over_charge_time_rate".into(),
            DataType::Float32,
        ),
        Field::new("creature_experience_amount_rate".into(), DataType::Float32),
        Field::new("creature_physical_critical_hit".into(), DataType::Float32),
        Field::new("creature_magical_critical_hit".into(), DataType::Float32),
        Field::new("creature_stuck".into(), DataType::Float32),
        // --- Strings ---
        Field::new("name".into(), DataType::String),
        Field::new("name2".into(), DataType::String),
        Field::new("equipment_type".into(), DataType::String),
        Field::new("item_group_name".into(), DataType::String),
        Field::new("set_name".into(), DataType::String),
        Field::new("item_category".into(), DataType::String),
        Field::new("armor_type".into(), DataType::String),
        Field::new("display_equipment_type".into(), DataType::String),
        Field::new("display_rarity".into(), DataType::String),
        Field::new("display_usable_job".into(), DataType::String),
        // --- Simple Lists (Vec<T>) ---
        Field::new(
            "usable_job".into(),
            DataType::List(Box::new(DataType::String)),
        ),
        Field::new(
            "usable_world".into(),
            DataType::List(Box::new(DataType::String)),
        ),
        Field::new(
            "difficulty_for_extra_drop".into(),
            DataType::List(Box::new(DataType::String)),
        ),
        Field::new(
            "dungeon_type_for_extra_drop".into(),
            DataType::List(Box::new(DataType::String)),
        ),
        Field::new("set_item".into(), DataType::List(Box::new(DataType::Int32))),
        Field::new(
            "enable_dye".into(),
            DataType::List(Box::new(DataType::Int32)),
        ),
        Field::new("int_data".into(), DataType::List(Box::new(DataType::Int32))),
        Field::new(
            "prof_additional_gain_exp".into(),
            DataType::List(Box::new(DataType::Int32)),
        ),
        Field::new(
            "prof_result_variation".into(),
            DataType::List(Box::new(DataType::Int32)),
        ),
        Field::new(
            "prof_disjoint_result_variation".into(),
            DataType::List(Box::new(DataType::Int32)),
        ),
        Field::new(
            "prof_material_variation".into(),
            DataType::List(Box::new(DataType::Int32)),
        ),
        // --- Complex Structs ---
        Field::new(
            "avatar_select_ability".into(),
            DataType::List(Box::new(get_avatar_select_ability_dtype())),
        ),
        Field::new("set_ability".into(), get_set_ability_dtype()),
        Field::new(
            "all_skill_item".into(),
            DataType::List(Box::new(get_all_skill_item_dtype())),
        ),
        Field::new("emancipate".into(), get_emancipate_dtype()),
        Field::new(
            "piece_set_ability".into(),
            DataType::List(Box::new(get_piece_set_ability_dtype())),
        ),
    ]);

    s.extend(get_stat_property_schema().iter_fields().collect::<Vec<_>>());

    Arc::new(s)
}

#[cfg(test)]
mod tests {
    use crate::entity::equipment::get_equipment_schema;
    use crate::entity::stat_property::get_stat_property_schema;

    #[test]
    fn check_duplicate_key() {
        let schema1 = get_stat_property_schema();
        let schema2 = get_equipment_schema();
        for name in schema1.iter_names() {
            if schema2.contains(name) {
                println!("Duplicate key: {}", name);
            }
        }

        for name in schema2.iter_names() {
            if schema1.contains(name) {
                println!("Duplicate key: {}", name);
            }
        }
    }
}
