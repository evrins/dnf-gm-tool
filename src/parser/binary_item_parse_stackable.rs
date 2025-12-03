use crate::entity::stackable::Stackable;
use crate::parser::binary_item::BinaryItem;
use crate::parser::binary_item_parser::BinaryItemParser;
use tracing::debug;

impl BinaryItemParser {
    pub fn parse_stackable(&mut self) -> Stackable {
        let mut res = Stackable::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[name]" => {
                        res.name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[name2]" => {
                        res.name2 = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[minimum level]" => {
                        res.minimum_level = *self.parse_next_one().as_int().unwrap();
                    }
                    "[rarity]" => {
                        res.rarity = *self.parse_next_one().as_int().unwrap();
                    }
                    "[stackable type]" => {
                        res.stackable_type = self.parse_next_one().as_string().unwrap().clone();
                        res.sub_stackable_type = *self.parse_next_one().as_int().unwrap();
                    }
                    "[item group name]" => {
                        res.item_group_name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[item category]" => {
                        res.item_category = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[stack limit]" => {
                        res.stack_limit = *self.parse_next_one().as_int().unwrap();
                    }
                    "[usable job]" => {
                        res.usable_job = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[enchant]" => {
                        res.enchant = self.parse_enchant();
                    }
                    "[stat desc]" => {
                        res.stat_desc = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[string data]" => {
                        res.string_data = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[monster card id]" => {
                        res.monster_card_id = *self.parse_next_one().as_int().unwrap();
                    }
                    _ => {
                        debug!("skip {:?} in parse stackable", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res.update_display_rarity();
        res.update_display_stackable_type();
        res.update_display_usable_job();

        if res.item_category == "monster card"
            && res.enchant.display_enchant_category.len() == 0
        {
            res.enchant.display_enchant_category = vec!["特殊效果".into()];
        }

        res
    }
}
