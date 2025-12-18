use crate::entity::all_skill_item::AllSkillItem;
use crate::entity::avatar_select_ability::AvatarSelectAbility;
use crate::entity::dungeon::Dungeon;
use crate::entity::emancipate::Emancipate;
use crate::entity::item_aura::ItemAura;
use crate::entity::piece_set::PieceSet;
use crate::entity::piece_set_ability::PieceSetAbility;
use crate::entity::set_ability::SetAbility;
use crate::entity::skill::Skill;
use crate::entity::skill_apply_condition::SkillApplyCondition;
use crate::entity::skill_level_up::SkillLevelUp;
use crate::parser::binary_item::BinaryItem;
use tracing::debug;

pub struct BinaryItemParser {
    pub binary_item_list: Vec<BinaryItem>,
    pub idx: usize,
    pub total: usize,
}

impl BinaryItemParser {
    pub fn new(binary_item_list: Vec<BinaryItem>) -> BinaryItemParser {
        let total = binary_item_list.len();

        Self {
            binary_item_list,
            idx: 0,
            total,
        }
    }

    pub fn parse_dungeon(&mut self) -> Dungeon {
        let mut dungeon = Dungeon::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[name]" => {
                        dungeon.name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[explain]" => {
                        dungeon.explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[basis level]" => {
                        dungeon.basis_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[minimum required level]" => {
                        dungeon.minimum_required_level = *self.parse_next_one().as_int().unwrap();
                    }
                    _ => {
                        debug!("skip {:?} in parse dungeon", segment);
                    }
                }
            }
            self.idx += 1;
        }

        dungeon
    }

    pub fn parse_skill(&mut self) -> Skill {
        let mut skill = Skill::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[name]" => {
                        skill.name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[name2]" => {
                        skill.explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[job]" => {
                        skill.job = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[basic explain]" => {
                        skill.basic_explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[explain]" => {
                        skill.explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[feature skill index]" => {
                        skill.feature_skill_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[skill class]" => {
                        skill.skill_class = *self.parse_next_one().as_int().unwrap();
                    }

                    _ => {
                        debug!("skip {:?} in parse skill", segment);
                    }
                }
            }
            self.idx += 1;
        }

        skill
    }

    pub fn parse_emancipate(&mut self) -> Emancipate {
        let mut res = Emancipate::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[input]" => {
                        res.input = self.parse_until_segment_as_int_list();
                    }
                    "[output]" => {
                        res.output = self.parse_until_segment_as_int_list();
                    }
                    "[emancipate explain]" => {
                        res.emancipate_explain = self.parse_next_one().as_string().unwrap().clone();
                    }
                    _ => {
                        debug!("skip {:?} in parse emancipate", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res
    }

    pub fn parse_all_skill_item(&mut self) -> AllSkillItem {
        let mut res = AllSkillItem::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[skill phase]" => {
                        res.skill_phase = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[item growtype]" => {
                        res.item_grow_type = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[skill apply condition]" => {
                        res.skill_apply_condition = self.parse_skill_apply_condition();
                    }
                    _ => {
                        debug!("skip {:?} in parse emancipate", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res
    }

    pub fn parse_skill_apply_condition(&mut self) -> SkillApplyCondition {
        let mut res = SkillApplyCondition::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[skill group]" => {
                        res.skill_group = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[lower bound level]" => {
                        res.lower_bound_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[upper bound level]" => {
                        res.upper_bound_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[value]" => {
                        res.value = *self.parse_next_one().as_int().unwrap();
                    }
                    "[extra condition]" => {
                        res.extra_condition = self.parse_until_segment_as_string_list();
                    }
                    _ => {
                        debug!("skip {:?} in parse skill apply condition", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res
    }

    pub fn parse_avatar_select_ability(&mut self) -> AvatarSelectAbility {
        let res = AvatarSelectAbility::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(_) = it {}
            self.idx += 1;
        }

        res
    }

    pub fn parse_item_aura(&mut self) -> ItemAura {
        ItemAura {
            aura_type: self.parse_next_one().as_string().unwrap().clone(),
            op: self.parse_next_one().as_string().unwrap().clone(),
            num: *self.parse_next_one().as_int().unwrap(),
            distance: *self.parse_next_one().as_int().unwrap(),
        }
    }

    pub fn parse_piece_set_ability(&mut self) -> PieceSetAbility {
        let res = PieceSetAbility {
            part_count: *self.parse_next_one().as_int().unwrap(),
            ..Default::default()
        };

        self.idx += 1;
        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[/piece set ability]" => {
                        break;
                    }
                    _ => {
                        debug!("skip {:?} in parse piece set ability", segment);
                    }
                }
            }
            self.idx += 1;
        }
        res
    }
    pub fn parse_skill_level_up_list(&mut self) -> Vec<SkillLevelUp> {
        let mut res = Vec::<SkillLevelUp>::new();
        while !matches!(self.binary_item_list[self.idx + 1], BinaryItem::Segment(_)) {
            res.push(SkillLevelUp {
                role: self.binary_item_list[self.idx + 1]
                    .as_string()
                    .unwrap()
                    .clone(),
                skill_id: *self.binary_item_list[self.idx + 2].as_int().unwrap(),
                level_up: *self.binary_item_list[self.idx + 3].as_int().unwrap(),
            });

            self.idx += 3;
        }
        self.idx += 1;

        res
    }

    pub fn parse_set_ability(&mut self) -> SetAbility {
        let mut res = SetAbility::default();
        self.idx += 1;
        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[set name]" => {
                        res.set_name = *self.parse_next_one().as_int().unwrap();
                    }
                    "[fullset basic explain]" => {
                        res.fullset_basic_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[fullset detail explain]" => {
                        res.fullset_detail_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[/set ability]" => {
                        break;
                    }
                    _ => {
                        debug!("skip {:?} in parse set ability", segment);
                    }
                }
            }
            self.idx += 1;
        }
        res
    }

    pub fn parse_piece_set(&mut self) -> PieceSet {
        let mut res = PieceSet::default();
        self.idx += 1;
        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[set name]" => {
                        res.set_name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[piece set ability]" => {
                        res.piece_set_ability.push(self.parse_piece_set_ability());
                    }
                    "[fullset detail explain]" => {
                        res.parameter_basic_explain =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[part set index]" => {
                        res.part_set_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[/set ability]" => {
                        break;
                    }
                    _ => {
                        debug!("skip {:?} in parse set", segment);
                    }
                }
            }
            self.idx += 1;
        }
        res
    }

    pub fn parse_next_one(&mut self) -> &BinaryItem {
        self.idx += 1;
        self.current_item()
    }

    pub fn parse_next_as_float(&mut self) -> f32 {
        match self.parse_next_one() {
            BinaryItem::Int(v) => *v as f32,
            BinaryItem::Float(v) => *v,
            _ => {
                panic!("wrong segment type")
            }
        }
    }

    pub fn parse_until_segment(&mut self) -> &[BinaryItem] {
        let start_index = self.idx;

        while self.idx < self.total - 1 && !matches!(self.next_n_item(1), BinaryItem::Segment(_)) {
            self.idx += 1;
        }

        &self.binary_item_list[start_index + 1..self.idx + 1]
    }

    pub fn parse_until_segment_as_int_list(&mut self) -> Vec<i32> {
        self.parse_until_segment()
            .iter()
            .map(|it| *it.as_int().unwrap())
            .collect()
    }

    pub fn parse_until_segment_as_uint_list(&mut self) -> Vec<u32> {
        self.parse_until_segment()
            .iter()
            .map(|it| *it.as_u_int().unwrap())
            .collect()
    }

    pub fn parse_until_segment_as_float_list(&mut self) -> Vec<f32> {
        self.parse_until_segment()
            .iter()
            .map(|it| *it.as_float().unwrap())
            .collect()
    }

    pub fn parse_until_segment_as_string_list(&mut self) -> Vec<String> {
        let item_list = self.parse_until_segment();
        item_list
            .iter()
            .map(|it| it.as_string().unwrap().clone())
            .collect()
    }

    pub fn current_item(&self) -> &BinaryItem {
        let idx = self.idx;
        &self.binary_item_list[idx]
    }

    pub fn next_n_item(&self, n: usize) -> &BinaryItem {
        &self.binary_item_list[self.idx + n]
    }

    pub fn to_string_list(&self) -> Vec<String> {
        self.binary_item_list
            .iter()
            .map(|it| match it {
                BinaryItem::Int(v) => v.to_string(),
                BinaryItem::UInt(v) => v.to_string(),
                BinaryItem::Float(v) => v.to_string(),
                BinaryItem::Segment(v) => format!("segment: {}", v),
                BinaryItem::String(v) => v.to_string(),
            })
            .collect()
    }
}
