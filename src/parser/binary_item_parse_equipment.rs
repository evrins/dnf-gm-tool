use crate::entity::equipment::Equipment;
use crate::entity::stat_property::StatProperty;
use crate::parser::binary_item::BinaryItem;
use crate::parser::binary_item_parser::BinaryItemParser;
use tracing::debug;

impl BinaryItemParser {
    pub fn parse_equipment(&mut self) -> Equipment {
        let mut res = Equipment::default();
        let mut sp = StatProperty::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[physical attack]" => {
                        sp.physical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[physical defense]" => {
                        sp.physical_defense = *self.parse_next_one().as_int().unwrap();
                    }
                    "[magical attack]" => {
                        sp.magical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[magical defense]" => {
                        sp.magical_defense = *self.parse_next_one().as_int().unwrap();
                    }
                    "[separate attack]" => {
                        sp.separate_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[HP MAX]" => {
                        sp.hp_max = *self.parse_next_one().as_int().unwrap();
                    }
                    "[MP MAX]" => {
                        sp.mp_max = *self.parse_next_one().as_int().unwrap();
                    }
                    "[HP MAX rate]" => {
                        sp.hp_max_rate = *self.parse_next_one().as_float().unwrap();
                    }
                    "[MP MAX rate]" => {
                        sp.mp_max_rate = *self.parse_next_one().as_float().unwrap();
                    }
                    "[HP regen speed]" => {
                        sp.hp_regen_speed = *self.parse_next_one().as_int().unwrap();
                    }
                    "[MP regen speed]" => {
                        sp.mp_regen_speed = *self.parse_next_one().as_int().unwrap();
                    }
                    "[move speed]" => {
                        sp.move_speed = *self.parse_next_one().as_int().unwrap();
                    }
                    "[attack speed]" => {
                        sp.attack_speed = *self.parse_next_one().as_int().unwrap();
                    }
                    "[cast speed]" => {
                        sp.cast_speed = *self.parse_next_one().as_int().unwrap();
                    }
                    "[stuck resistance]" => {
                        sp.stuck_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[stuck]" => {
                        sp.stuck = self.parse_next_as_float();
                    }
                    "[stun resistance]" => {
                        sp.stun_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[piercing resistance]" => {
                        sp.piercing_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[freeze resistance]" => {
                        sp.freeze_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[confuse resistance]" => {
                        sp.confuse_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[poison resistance]" => {
                        sp.poison_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[blind resistance]" => {
                        sp.blind_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[stone resistance]" => {
                        sp.stone_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[curse resistance]" => {
                        sp.curse_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[bleeding resistance]" => {
                        sp.bleeding_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[lightning resistance]" => {
                        sp.lightning_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[burn resistance]" => {
                        sp.burn_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[sleep resistance]" => {
                        sp.sleep_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[slow resistance]" => {
                        sp.slow_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[hold resistance]" => {
                        sp.hold_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[all elemental attack]" => {
                        sp.all_elemental_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[all elemental resistance]" => {
                        sp.all_elemental_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[all activestatus resistance]" => {
                        sp.all_activestatus_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[room list move speed rate]" => {
                        sp.room_list_move_speed_rate = *self.parse_next_one().as_float().unwrap();
                    }
                    "[parameter basic explain]" => {
                        sp.parameter_basic_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[parameter detail explain]" => {
                        sp.parameter_detail_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[fullset explain]" => {
                        sp.fullset_explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[jump power]" => {
                        sp.jump_power = *self.parse_next_one().as_int().unwrap();
                    }
                    "[physical critical hit]" => {
                        sp.physical_critical_hit = self.parse_next_as_float();
                    }
                    "[magical critical hit]" => {
                        sp.magical_critical_hit = self.parse_next_as_float();
                    }
                    "[equipment physical attack]" => {
                        sp.equipment_physical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[equipment magical attack]" => {
                        sp.equipment_magical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[equipment physical defense]" => {
                        sp.equipment_physical_defense = *self.parse_next_one().as_int().unwrap();
                    }
                    "[equipment magical defense]" => {
                        sp.equipment_magical_defense = *self.parse_next_one().as_int().unwrap();
                    }
                    "[dark attack]" => {
                        sp.dark_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[light attack]" => {
                        sp.light_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[fire attack]" => {
                        sp.fire_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[water attack]" => {
                        sp.water_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[dark resistance]" => {
                        sp.dark_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[light resistance]" => {
                        sp.light_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[fire resistance]" => {
                        sp.fire_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[water resistance]" => {
                        sp.water_resistance = *self.parse_next_one().as_int().unwrap();
                    }
                    "[anti evil]" => {
                        sp.anti_evil = *self.parse_next_one().as_int().unwrap();
                    }
                    "[hit recovery]" => {
                        sp.hit_recovery = *self.parse_next_one().as_int().unwrap();
                    }
                    "[skill levelup]" => {
                        sp.skill_level_up = self.parse_skill_level_up_list();
                    }
                    "[item aura]" => {
                        sp.item_aura.push(self.parse_item_aura());
                    }
                    "[basic explain]" => {
                        sp.basic_explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[detail explain]" => {
                        sp.detail_explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[flavor text]" => {
                        sp.flavor_text = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[explain]" => {
                        sp.explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[fullset basic explain]" => {
                        sp.fullset_basic_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[fullset detail explain]" => {
                        sp.fullset_detail_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[elemental property]" => {
                        sp.elemental_property = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[MP regen speed rate]" => {
                        sp.mp_regen_speed_rate = *self.parse_next_one().as_int().unwrap();
                    }
                    "[HP regen speed rate]" => {
                        sp.hp_regen_speed_rate = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature magical attack]" => {
                        sp.creature_magical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature physical attack]" => {
                        sp.creature_physical_attack = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature skill charge time rate]" => {
                        sp.creature_skill_charge_time_rate =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[rigidity]" => {
                        sp.rigidity = *self.parse_next_one().as_int().unwrap();
                    }
                    "[lift up]" => {
                        sp.lift_up = *self.parse_next_one().as_int().unwrap();
                    }

                    "[piece set ability]" => {
                        res.piece_set_ability.push(self.parse_piece_set_ability());
                    }
                    "[grade]" => {
                        res.grade = *self.parse_next_one().as_int().unwrap();
                    }
                    "[sub type]" => {
                        res.sub_type = *self.parse_next_one().as_int().unwrap();
                    }
                    "[int data]" => {
                        res.int_data = self.parse_until_segment_as_int_list();
                    }
                    "[name]" => {
                        res.name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[name2]" => {
                        res.name2 = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[rarity]" => {
                        res.rarity = *self.parse_next_one().as_int().unwrap();
                    }
                    "[usable job]" => {
                        res.usable_job = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[minimum level]" => {
                        res.minimum_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[maximum level]" => {
                        res.maximum_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[price]" => {
                        res.price = *self.parse_next_one().as_int().unwrap();
                    }
                    "[repair price]" => {
                        res.repair_price = *self.parse_next_one().as_int().unwrap();
                    }
                    "[value]" => {
                        res.value = *self.parse_next_one().as_int().unwrap();
                    }
                    "[equipment type]" => {
                        res.equipment_type = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[durability]" => {
                        res.durability = *self.parse_next_one().as_int().unwrap();
                    }
                    "[weight]" => {
                        res.weight = *self.parse_next_one().as_int().unwrap();
                    }
                    "[item group name]" => {
                        res.item_group_name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[cool time]" => {
                        res.cool_time = *self.parse_next_one().as_int().unwrap();
                    }

                    "[set item]" => {
                        res.set_item = self.parse_until_segment_as_int_list();
                    }
                    "[set ability]" => {
                        res.set_ability = self.parse_set_ability();
                    }

                    "[enable dye]" => {
                        res.enable_dye = self.parse_until_segment_as_int_list();
                    }
                    "[part set index]" => {
                        res.part_set_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[set item master]" => {
                        res.set_item_master = *self.parse_next_one().as_int().unwrap();
                    }
                    "[avatar select ability]" => {
                        res.avatar_select_ability
                            .push(self.parse_avatar_select_ability());
                    }
                    "[item category]" => {
                        res.item_category = self.parse_next_one().as_string().unwrap().clone();
                        self.idx += 1;
                    }
                    "[all skill item]" => {
                        res.all_skill_item.push(self.parse_all_skill_item());
                    }
                    "[push aside]" => {
                        res.push_aside = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature species]" => {
                        res.creature_species = *self.parse_next_one().as_int().unwrap();
                    }
                    "[output index]" => {
                        res.output_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[cash]" => {
                        res.cash = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature minimum level]" => {
                        res.creature_min_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[creature skill consume mp rate]" => {
                        res.creature_skill_consume_mp_rate =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[creature skill over charge time rate]" => {
                        res.creature_skill_over_charge_time_rate =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[creature experience amount rate]" => {
                        res.creature_experience_amount_rate =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[creature physical critical hit]" => {
                        res.creature_physical_critical_hit =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[creature magical critical hit]" => {
                        res.creature_magical_critical_hit =
                            *self.parse_next_one().as_float().unwrap();
                    }
                    "[creature stuck]" => {
                        res.creature_stuck = *self.parse_next_one().as_float().unwrap();
                    }
                    "[emancipate]" => {
                        res.emancipate = self.parse_emancipate();
                    }

                    "[minimum rank]" => {
                        res.minimum_rank = *self.parse_next_one().as_int().unwrap();
                    }
                    "[usable world]" => {
                        res.usable_world = self.parse_until_segment_as_string_list();
                    }
                    "[prof compound rate]" => {
                        res.prof_compound_rate = *self.parse_next_one().as_int().unwrap();
                    }
                    "[prof additional gain exp]" => {
                        res.prof_additional_gain_exp = self.parse_until_segment_as_int_list();
                    }
                    "[prof result variation]" => {
                        res.prof_result_variation = self.parse_until_segment_as_int_list();
                    }
                    "[prof disjoint result variation]" => {
                        res.prof_disjoint_result_variation = self.parse_until_segment_as_int_list();
                    }
                    "[prof material variation]" => {
                        res.prof_material_variation = self.parse_until_segment_as_int_list();
                    }

                    "[set name]" => {
                        res.set_name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[aurora avatar]" => {
                        res.aurora_avatar = *self.parse_next_one().as_int().unwrap();
                    }
                    "[clear avatar]" => {
                        res.clear_avatar = *self.parse_next_one().as_int().unwrap();
                    }
                    "[special monster drop]" => {
                        res.special_monster_drop = *self.parse_next_one().as_int().unwrap();
                    }
                    "[difficulty for extra drop]" => {
                        res.difficulty_for_extra_drop = self.parse_until_segment_as_string_list();
                    }
                    "[dungeon type for extra drop]" => {
                        res.dungeon_type_for_extra_drop = self.parse_until_segment_as_string_list();
                    }

                    _ => {
                        debug!("skip {:?} in parse equipment", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res.stat_property = sp;

        res.update_armor_type();
        res.update_display_rarity();
        res.update_display_equipment_type();
        res.update_display_usable_job();

        res
    }
}
