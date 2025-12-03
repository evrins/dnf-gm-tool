use crate::entity::all_skill_item_container::AllSkillItemContainer;
use crate::parser::binary_item::BinaryItem;
use crate::parser::binary_item_parser::BinaryItemParser;
use tracing::debug;

impl BinaryItemParser {
    pub fn parse_all_skill_item_container(&mut self) -> AllSkillItemContainer {
        let mut res = AllSkillItemContainer::default();

        self.idx += 1;
        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[/all skill item container]" => {
                        break;
                    }
                    "[all skill item]" => {
                        res.all_skill_item = self.parse_all_skill_item();
                    }
                    _ => {
                        debug!("key skipped {} in parse all skill item container", segment);
                    }
                }
            }
            self.idx += 1;
        }

        res
    }
}
