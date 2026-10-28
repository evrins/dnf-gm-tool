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
                        dungeon.name = self.next_str();
                    }
                    "[explain]" => {
                        dungeon.explain = self.next_str();
                    }
                    "[basis level]" => {
                        dungeon.basis_level = self.next_int();
                    }
                    "[minimum required level]" => {
                        dungeon.minimum_required_level = self.next_int();
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
                        skill.name = self.next_str();
                    }
                    "[name2]" => {
                        skill.explain = self.next_str();
                    }
                    "[job]" => {
                        skill.job = self.next_str();
                    }
                    "[basic explain]" => {
                        skill.basic_explain = self.next_str();
                    }
                    "[explain]" => {
                        skill.explain = self.next_str();
                    }
                    "[feature skill index]" => {
                        skill.feature_skill_index = self.next_int();
                    }
                    "[skill class]" => {
                        skill.skill_class = self.next_int();
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
                        res.emancipate_explain = self.next_str();
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
                        res.skill_phase = self.next_str();
                    }
                    "[item growtype]" => {
                        res.item_grow_type = self.next_str();
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
                        res.skill_group = self.next_str();
                    }
                    "[lower bound level]" => {
                        res.lower_bound_level = self.next_int();
                    }
                    "[upper bound level]" => {
                        res.upper_bound_level = self.next_int();
                    }
                    "[value]" => {
                        res.value = self.next_int();
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
            aura_type: self.next_str(),
            op: self.next_str(),
            num: self.next_int(),
            distance: self.next_int(),
        }
    }

    pub fn parse_piece_set_ability(&mut self) -> PieceSetAbility {
        let res = PieceSetAbility {
            part_count: self.next_int(),
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

        // Records are (role, skill id, level up) triples terminated by a segment.
        while self.idx + 3 < self.total {
            let Some(role) = self.item_at(self.idx + 1).and_then(BinaryItem::as_text) else {
                break;
            };
            if self.next_n_item(1).is_segment() {
                break;
            }

            let skill_id = self
                .item_at(self.idx + 2)
                .and_then(BinaryItem::as_int_value)
                .unwrap_or_default();
            let level_up = self
                .item_at(self.idx + 3)
                .and_then(BinaryItem::as_int_value)
                .unwrap_or_default();

            res.push(SkillLevelUp {
                role: role.to_string(),
                skill_id,
                level_up,
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
                        res.set_name = self.next_int();
                    }
                    "[fullset basic explain]" => {
                        res.fullset_basic_explain = self.next_str();
                    }
                    "[fullset detail explain]" => {
                        res.fullset_detail_explain = self.next_str();
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
                        res.set_name = self.next_str();
                    }
                    "[piece set ability]" => {
                        res.piece_set_ability.push(self.parse_piece_set_ability());
                    }
                    "[fullset detail explain]" => {
                        res.parameter_basic_explain = self.next_str();
                    }
                    "[part set index]" => {
                        res.part_set_index = self.next_int();
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

    /// Move to the next item and return it.
    ///
    /// Returns a neutral placeholder when the payload ends in the middle of a
    /// record instead of panicking; use the typed `next_*` accessors below.
    pub fn parse_next_one(&mut self) -> &BinaryItem {
        self.idx += 1;
        self.current_item()
    }

    /// Move to the next item and read it as text (empty when it is not a value).
    pub fn next_str(&mut self) -> String {
        self.idx += 1;
        self.item_at(self.idx)
            .and_then(BinaryItem::as_text)
            .unwrap_or_default()
            .to_string()
    }

    /// Move to the next item and read it as an integer (0 when it is not a value).
    pub fn next_int(&mut self) -> i32 {
        self.idx += 1;
        self.item_at(self.idx)
            .and_then(BinaryItem::as_int_value)
            .unwrap_or_default()
    }

    /// Move to the next item and read it as an unsigned integer.
    pub fn next_uint(&mut self) -> u32 {
        self.idx += 1;
        self.item_at(self.idx)
            .and_then(BinaryItem::as_uint_value)
            .unwrap_or_default()
    }

    /// Move to the next item and read it as a float (integers are converted).
    pub fn next_float(&mut self) -> f32 {
        self.idx += 1;
        self.item_at(self.idx)
            .and_then(BinaryItem::as_float_value)
            .unwrap_or_default()
    }

    /// Move to the next item and read it as a segment (empty when it is not one).
    pub fn next_segment(&mut self) -> String {
        self.idx += 1;
        match self.item_at(self.idx) {
            Some(BinaryItem::Segment(value)) => value.clone(),
            _ => String::new(),
        }
    }

    /// Legacy alias of [`BinaryItemParser::next_float`].
    pub fn parse_next_as_float(&mut self) -> f32 {
        self.next_float()
    }

    /// Collect every item up to the next segment.
    ///
    /// The cursor is left on the last collected item, exactly like before, so
    /// the caller keeps control of the following `idx += 1`.
    pub fn parse_until_segment(&mut self) -> &[BinaryItem] {
        let start = (self.idx + 1).min(self.total);
        let mut end = start;

        while end < self.total && !self.binary_item_list[end].is_segment() {
            end += 1;
        }

        self.idx = end.saturating_sub(1);
        &self.binary_item_list[start..end]
    }

    pub fn parse_until_segment_as_int_list(&mut self) -> Vec<i32> {
        self.parse_until_segment()
            .iter()
            .filter_map(BinaryItem::as_int_value)
            .collect()
    }

    pub fn parse_until_segment_as_uint_list(&mut self) -> Vec<u32> {
        self.parse_until_segment()
            .iter()
            .filter_map(BinaryItem::as_uint_value)
            .collect()
    }

    pub fn parse_until_segment_as_float_list(&mut self) -> Vec<f32> {
        self.parse_until_segment()
            .iter()
            .filter_map(BinaryItem::as_float_value)
            .collect()
    }

    pub fn parse_until_segment_as_string_list(&mut self) -> Vec<String> {
        self.parse_until_segment()
            .iter()
            .filter_map(|item| item.as_text().map(str::to_string))
            .collect()
    }

    /// Item at `index`, or `None` when the index is out of range.
    pub fn item_at(&self, index: usize) -> Option<&BinaryItem> {
        self.binary_item_list.get(index)
    }

    pub fn current_item(&self) -> &BinaryItem {
        self.item_at(self.idx).unwrap_or(&PLACEHOLDER_ITEM)
    }

    pub fn next_n_item(&self, n: usize) -> &BinaryItem {
        self.item_at(self.idx + n).unwrap_or(&PLACEHOLDER_ITEM)
    }

    pub fn to_string_list(&self) -> Vec<String> {
        self.binary_item_list
            .iter()
            .map(BinaryItem::to_display_string)
            .collect()
    }
}

/// Returned by the accessors when a payload ends in the middle of a record.
static PLACEHOLDER_ITEM: BinaryItem = BinaryItem::Int(0);
