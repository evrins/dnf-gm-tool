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
                        sp.physical_attack = self.next_int();
                    }
                    "[physical defense]" => {
                        sp.physical_defense = self.next_int();
                    }
                    "[magical attack]" => {
                        sp.magical_attack = self.next_int();
                    }
                    "[magical defense]" => {
                        sp.magical_defense = self.next_int();
                    }
                    "[separate attack]" => {
                        sp.separate_attack = self.next_int();
                    }
                    "[HP MAX]" => {
                        sp.hp_max = self.next_int();
                    }
                    "[MP MAX]" => {
                        sp.mp_max = self.next_int();
                    }
                    "[HP MAX rate]" => {
                        sp.hp_max_rate = self.next_float();
                    }
                    "[MP MAX rate]" => {
                        sp.mp_max_rate = self.next_float();
                    }
                    "[HP regen speed]" => {
                        sp.hp_regen_speed = self.next_int();
                    }
                    "[MP regen speed]" => {
                        sp.mp_regen_speed = self.next_int();
                    }
                    "[move speed]" => {
                        sp.move_speed = self.next_int();
                    }
                    "[attack speed]" => {
                        sp.attack_speed = self.next_int();
                    }
                    "[cast speed]" => {
                        sp.cast_speed = self.next_int();
                    }
                    "[stuck resistance]" => {
                        sp.stuck_resistance = self.next_int();
                    }
                    "[stuck]" => {
                        sp.stuck = self.next_float();
                    }
                    "[stun resistance]" => {
                        sp.stun_resistance = self.next_int();
                    }
                    "[piercing resistance]" => {
                        sp.piercing_resistance = self.next_int();
                    }
                    "[freeze resistance]" => {
                        sp.freeze_resistance = self.next_int();
                    }
                    "[confuse resistance]" => {
                        sp.confuse_resistance = self.next_int();
                    }
                    "[poison resistance]" => {
                        sp.poison_resistance = self.next_int();
                    }
                    "[blind resistance]" => {
                        sp.blind_resistance = self.next_int();
                    }
                    "[stone resistance]" => {
                        sp.stone_resistance = self.next_int();
                    }
                    "[curse resistance]" => {
                        sp.curse_resistance = self.next_int();
                    }
                    "[bleeding resistance]" => {
                        sp.bleeding_resistance = self.next_int();
                    }
                    "[lightning resistance]" => {
                        sp.lightning_resistance = self.next_int();
                    }
                    "[burn resistance]" => {
                        sp.burn_resistance = self.next_int();
                    }
                    "[sleep resistance]" => {
                        sp.sleep_resistance = self.next_int();
                    }
                    "[slow resistance]" => {
                        sp.slow_resistance = self.next_int();
                    }
                    "[hold resistance]" => {
                        sp.hold_resistance = self.next_int();
                    }
                    "[all elemental attack]" => {
                        sp.all_elemental_attack = self.next_int();
                    }
                    "[all elemental resistance]" => {
                        sp.all_elemental_resistance = self.next_int();
                    }
                    "[all activestatus resistance]" => {
                        sp.all_activestatus_resistance = self.next_int();
                    }
                    "[room list move speed rate]" => {
                        sp.room_list_move_speed_rate = self.next_float();
                    }
                    "[parameter basic explain]" => {
                        sp.parameter_basic_explain = self.next_str();
                    }
                    "[parameter detail explain]" => {
                        sp.parameter_detail_explain = self.next_str();
                    }
                    "[fullset explain]" => {
                        sp.fullset_explain = self.next_str();
                    }
                    "[jump power]" => {
                        sp.jump_power = self.next_int();
                    }
                    "[physical critical hit]" => {
                        sp.physical_critical_hit = self.next_float();
                    }
                    "[magical critical hit]" => {
                        sp.magical_critical_hit = self.next_float();
                    }
                    "[equipment physical attack]" => {
                        sp.equipment_physical_attack = self.next_int();
                    }
                    "[equipment magical attack]" => {
                        sp.equipment_magical_attack = self.next_int();
                    }
                    "[equipment physical defense]" => {
                        sp.equipment_physical_defense = self.next_int();
                    }
                    "[equipment magical defense]" => {
                        sp.equipment_magical_defense = self.next_int();
                    }
                    "[dark attack]" => {
                        sp.dark_attack = self.next_int();
                    }
                    "[light attack]" => {
                        sp.light_attack = self.next_int();
                    }
                    "[fire attack]" => {
                        sp.fire_attack = self.next_int();
                    }
                    "[water attack]" => {
                        sp.water_attack = self.next_int();
                    }
                    "[dark resistance]" => {
                        sp.dark_resistance = self.next_int();
                    }
                    "[light resistance]" => {
                        sp.light_resistance = self.next_int();
                    }
                    "[fire resistance]" => {
                        sp.fire_resistance = self.next_int();
                    }
                    "[water resistance]" => {
                        sp.water_resistance = self.next_int();
                    }
                    "[anti evil]" => {
                        sp.anti_evil = self.next_int();
                    }
                    "[hit recovery]" => {
                        sp.hit_recovery = self.next_int();
                    }
                    "[skill levelup]" => {
                        sp.skill_level_up = self.parse_skill_level_up_list();
                    }
                    "[item aura]" => {
                        sp.item_aura.push(self.parse_item_aura());
                    }
                    "[basic explain]" => {
                        sp.basic_explain = self.next_str();
                    }
                    "[detail explain]" => {
                        sp.detail_explain = self.next_str();
                    }
                    "[flavor text]" => {
                        sp.flavor_text = self.next_str();
                    }
                    "[explain]" => {
                        sp.explain = self.next_str();
                    }
                    "[fullset basic explain]" => {
                        sp.fullset_basic_explain = self.next_str();
                    }
                    "[fullset detail explain]" => {
                        sp.fullset_detail_explain = self.next_str();
                    }
                    "[elemental property]" => {
                        sp.elemental_property = self.next_str();
                    }
                    "[MP regen speed rate]" => {
                        sp.mp_regen_speed_rate = self.next_int();
                    }
                    "[HP regen speed rate]" => {
                        sp.hp_regen_speed_rate = self.next_int();
                    }
                    "[creature magical attack]" => {
                        sp.creature_magical_attack = self.next_int();
                    }
                    "[creature physical attack]" => {
                        sp.creature_physical_attack = self.next_int();
                    }
                    "[creature skill charge time rate]" => {
                        sp.creature_skill_charge_time_rate = self.next_float();
                    }
                    "[rigidity]" => {
                        sp.rigidity = self.next_int();
                    }
                    "[inventory limit]" => {
                        sp.inventory_limit = self.next_int();
                    }
                    "[lift up]" => {
                        sp.lift_up = self.next_int();
                    }

                    "[piece set ability]" => {
                        res.piece_set_ability.push(self.parse_piece_set_ability());
                    }
                    "[grade]" => {
                        res.grade = self.next_int();
                    }
                    "[sub type]" => {
                        res.sub_type = self.next_int();
                    }
                    "[int data]" => {
                        res.int_data = self.parse_until_segment_as_int_list();
                    }
                    "[name]" => {
                        res.name = self.next_str();
                    }
                    "[name2]" => {
                        res.name2 = self.next_str();
                    }
                    "[attach type]" => {
                        res.attach_type = self.next_str();
                    }
                    "[rarity]" => {
                        res.rarity = self.next_int();
                    }
                    "[usable job]" => {
                        res.usable_job = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[minimum level]" => {
                        res.minimum_level = self.next_int();
                    }
                    "[maximum level]" => {
                        res.maximum_level = self.next_int();
                    }
                    "[price]" => {
                        res.price = self.next_int();
                    }
                    "[repair price]" => {
                        res.repair_price = self.next_int();
                    }
                    "[value]" => {
                        res.value = self.next_int();
                    }
                    "[equipment type]" => {
                        res.equipment_type = self.next_str();
                    }
                    "[durability]" => {
                        res.durability = self.next_int();
                    }
                    "[weight]" => {
                        res.weight = self.next_int();
                    }
                    "[item group name]" => {
                        res.item_group_name = self.next_str();
                    }
                    "[cool time]" => {
                        res.cool_time = self.next_int();
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
                        res.part_set_index = self.next_int();
                    }
                    "[set item master]" => {
                        res.set_item_master = self.next_int();
                    }
                    "[avatar select ability]" => {
                        res.avatar_select_ability
                            .push(self.parse_avatar_select_ability());
                    }
                    "[item category]" => {
                        res.item_category = self.next_str();
                        self.idx += 1;
                    }
                    "[all skill item]" => {
                        res.all_skill_item.push(self.parse_all_skill_item());
                    }
                    "[push aside]" => {
                        res.push_aside = self.next_int();
                    }
                    "[creature species]" => {
                        res.creature_species = self.next_int();
                    }
                    "[output index]" => {
                        res.output_index = self.next_int();
                    }
                    "[cash]" => {
                        res.cash = self.next_int();
                    }
                    "[creature minimum level]" => {
                        res.creature_min_level = self.next_int();
                    }
                    "[creature skill consume mp rate]" => {
                        res.creature_skill_consume_mp_rate = self.next_float();
                    }
                    "[creature skill over charge time rate]" => {
                        res.creature_skill_over_charge_time_rate = self.next_float();
                    }
                    "[creature experience amount rate]" => {
                        res.creature_experience_amount_rate = self.next_float();
                    }
                    "[creature physical critical hit]" => {
                        res.creature_physical_critical_hit = self.next_float();
                    }
                    "[creature magical critical hit]" => {
                        res.creature_magical_critical_hit = self.next_float();
                    }
                    "[creature stuck]" => {
                        res.creature_stuck = self.next_float();
                    }
                    "[emancipate]" => {
                        res.emancipate = self.parse_emancipate();
                    }

                    "[minimum rank]" => {
                        res.minimum_rank = self.next_int();
                    }
                    "[usable world]" => {
                        res.usable_world = self.parse_until_segment_as_string_list();
                    }
                    "[prof compound rate]" => {
                        res.prof_compound_rate = self.next_int();
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
                        res.set_name = self.next_str();
                    }
                    "[aurora avatar]" => {
                        res.aurora_avatar = self.next_int();
                    }
                    "[clear avatar]" => {
                        res.clear_avatar = self.next_int();
                    }
                    "[special monster drop]" => {
                        res.special_monster_drop = self.next_int();
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
        res.update_display_attach_type();

        res
    }
}
