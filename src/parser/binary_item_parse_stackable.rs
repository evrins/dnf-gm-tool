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
                        res.name = self.next_str();
                    }
                    "[name2]" => {
                        res.name2 = self.next_str();
                    }
                    "[minimum level]" => {
                        res.minimum_level = self.next_int();
                    }
                    "[rarity]" => {
                        res.rarity = self.next_int();
                    }
                    "[stackable type]" => {
                        res.stackable_type = self.next_str();
                        res.sub_stackable_type = self.next_int();
                    }
                    "[item group name]" => {
                        res.item_group_name = self.next_str();
                    }
                    "[item category]" => {
                        res.item_category = self.next_str();
                    }
                    "[stack limit]" => {
                        res.stack_limit = self.next_int();
                    }
                    "[usable job]" => {
                        res.usable_job = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[enchant]" => {
                        res.enchant = self.parse_enchant();
                    }
                    "[stat desc]" => {
                        res.stat_desc = self.next_str();
                    }
                    "[string data]" => {
                        res.string_data = self.parse_until_segment_as_string_list();
                        self.idx += 1;
                    }
                    "[monster card id]" => {
                        res.monster_card_id = self.next_int();
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

        if res.item_category == "monster card" && res.enchant.display_enchant_category.is_empty() {
            res.enchant.display_enchant_category = vec!["特殊效果".into()];
        }

        res
    }
}
