use crate::entity::enchant::Enchant;
use crate::entity::stat_property::StatProperty;
use crate::parser::binary_item::BinaryItem;
use crate::parser::binary_item_parser::BinaryItemParser;
use tracing::debug;

impl BinaryItemParser {
    pub fn parse_enchant(&mut self) -> Enchant {
        let mut res = Enchant::default();
        let mut sp = StatProperty::default();

        let mut segment_list = vec![];
        self.idx += 1;
        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                segment_list.push(segment.clone());

                match segment.as_str() {
                    "[/enchant]" => {
                        break;
                    }
                    "[physical attack]" => {
                        sp.physical_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("力量".into());
                    }
                    "[physical defense]" => {
                        sp.physical_defense = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("体力".into());
                    }
                    "[magical attack]" => {
                        sp.magical_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("智力".into());
                    }
                    "[magical defense]" => {
                        sp.magical_defense = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("精神".into());
                    }
                    "[separate attack]" => {
                        sp.separate_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("独立攻击力".into());
                    }
                    "[HP MAX]" => {
                        sp.hp_max = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("HP 最大值".into());
                    }
                    "[MP MAX]" => {
                        sp.mp_max = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("MP 最大值".into());
                    }
                    "[HP MAX rate]" => {
                        sp.hp_max_rate = *self.parse_next_one().as_float().unwrap();
                        res.display_enchant_category.push("[HP MAX rate]".into());
                    }
                    "[MP MAX rate]" => {
                        sp.mp_max_rate = *self.parse_next_one().as_float().unwrap();
                        res.display_enchant_category.push("[MP MAX rate]".into());
                    }
                    "[HP regen speed]" => {
                        sp.hp_regen_speed = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("HP 回复速度".into());
                    }
                    "[MP regen speed]" => {
                        sp.mp_regen_speed = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("MP 回复速度".into());
                    }
                    "[move speed]" => {
                        sp.move_speed = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("移动速度".into());
                    }
                    "[attack speed]" => {
                        sp.attack_speed = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("攻击速度".into());
                    }
                    "[cast speed]" => {
                        sp.cast_speed = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("释放速度".into());
                    }
                    "[stuck resistance]" => {
                        sp.stuck_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("回避率".into());
                    }
                    "[stuck]" => {
                        sp.stuck = self.parse_next_as_float();
                        res.display_enchant_category.push("命中率".into());
                    }
                    "[stun resistance]" => {
                        sp.stun_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("眩晕抗性".into());
                    }
                    "[piercing resistance]" => {
                        sp.piercing_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("穿刺抗性".into());
                    }
                    "[freeze resistance]" => {
                        sp.freeze_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("冰冻抗性".into());
                    }
                    "[confuse resistance]" => {
                        sp.confuse_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("混乱抗性".into());
                    }
                    "[poison resistance]" => {
                        sp.poison_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("中毒抗性".into());
                    }
                    "[blind resistance]" => {
                        sp.blind_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("致盲抗性".into());
                    }
                    "[stone resistance]" => {
                        sp.stone_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("石化抗性".into());
                    }
                    "[curse resistance]" => {
                        sp.curse_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("诅咒抗性".into());
                    }
                    "[bleeding resistance]" => {
                        sp.bleeding_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("出血抗性".into());
                    }
                    "[lightning resistance]" => {
                        sp.lightning_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("感电抗性".into());
                    }
                    "[burn resistance]" => {
                        sp.burn_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("灼烧抗性".into());
                    }
                    "[sleep resistance]" => {
                        sp.sleep_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("睡眠抗性".into());
                    }
                    "[slow resistance]" => {
                        sp.slow_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("减速抗性".into());
                    }
                    "[hold resistance]" => {
                        sp.hold_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("束缚抗性".into());
                    }
                    "[all elemental attack]" => {
                        sp.all_elemental_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("所有属性强化".into());
                    }
                    "[all elemental resistance]" => {
                        sp.all_elemental_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("所有属性抗性".into());
                    }
                    "[all activestatus resistance]" => {
                        sp.all_activestatus_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("所有异常状态抗性".into());
                    }
                    "[room list move speed rate]" => {
                        sp.room_list_move_speed_rate = *self.parse_next_one().as_float().unwrap();
                        res.display_enchant_category.push("地图移动速度".into());
                    }
                    "[jump power]" => {
                        sp.jump_power = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("跳跃力".into());
                    }
                    "[physical critical hit]" => {
                        sp.physical_critical_hit = self.parse_next_as_float();
                        res.display_enchant_category.push("物理暴击率".into());
                    }
                    "[magical critical hit]" => {
                        sp.magical_critical_hit = self.parse_next_as_float();
                        res.display_enchant_category.push("魔法暴击率".into());
                    }
                    "[equipment physical attack]" => {
                        sp.equipment_physical_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("物理攻击力".into());
                    }
                    "[equipment magical attack]" => {
                        sp.equipment_magical_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("魔法攻击力".into());
                    }
                    "[equipment physical defense]" => {
                        sp.equipment_physical_defense = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("物理防御力".into());
                    }
                    "[equipment magical defense]" => {
                        sp.equipment_magical_defense = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("魔法防御力".into());
                    }
                    "[dark attack]" => {
                        sp.dark_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("暗属性强化".into());
                    }
                    "[light attack]" => {
                        sp.light_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("光属性强化".into());
                    }
                    "[fire attack]" => {
                        sp.fire_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("火属性强化".into());
                    }
                    "[water attack]" => {
                        sp.water_attack = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("冰属性强化".into());
                    }
                    "[dark resistance]" => {
                        sp.dark_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("暗属性抗性".into());
                    }
                    "[light resistance]" => {
                        sp.light_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("光属性抗性".into());
                    }
                    "[fire resistance]" => {
                        sp.fire_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("火属性抗性".into());
                    }
                    "[water resistance]" => {
                        sp.water_resistance = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("冰属性抗性".into());
                    }
                    "[anti evil]" => {
                        sp.anti_evil = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("抗魔值".into());
                    }
                    "[rigidity]" => {
                        sp.rigidity = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("僵直".into());
                    }
                    "[hit recovery]" => {
                        sp.hit_recovery = *self.parse_next_one().as_int().unwrap();
                        res.display_enchant_category.push("硬直".into());
                    }
                    "[elemental property]" => {
                        sp.elemental_property = self.parse_next_one().as_string().unwrap().clone();
                        res.display_enchant_category.push("属性攻击".into());
                    }
                    "[skill levelup]" => {
                        sp.skill_level_up = self.parse_skill_level_up_list();
                        res.display_enchant_category.push("技能等级提升".into());
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
                    "[all skill item container]" => {
                        sp.all_skill_item_container = self.parse_all_skill_item_container();
                    }
                    _ => {
                        debug!("key skipped {} in parse enchant", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res.stat_property = sp;

        res.sort_display_enchant_category();

        res
    }
}
