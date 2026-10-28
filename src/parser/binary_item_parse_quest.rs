use crate::entity::quest::Quest;
use crate::parser::binary_item::BinaryItem;
use crate::parser::binary_item_parser::BinaryItemParser;
use tracing::debug;

impl BinaryItemParser {
    pub fn parse_quest(&mut self) -> Quest {
        let mut quest = Quest::default();

        while self.idx < self.total {
            let it = self.current_item();
            if let BinaryItem::Segment(segment) = it {
                match segment.as_str() {
                    "[name]" => {
                        quest.name = self.next_str();
                    }
                    "[grade]" => {
                        // stored as a plain string holding a bracketed value ("[epic]")
                        quest.grade = self.next_str();
                    }
                    "[sub type]" => {
                        quest.sub_type = self.next_int();
                    }
                    "[difficulty]" => {
                        quest.difficulty = self.next_str();
                    }
                    "[gold multiple]" => {
                        quest.gold_multiple = self.next_int();
                    }
                    "[npc index]" => {
                        quest.npc_index = self.next_int();
                    }
                    "[complete npc index]" => {
                        quest.complete_npc_index = self.next_int();
                    }
                    "[job]" => {
                        quest.job = self.next_str();
                    }
                    "[grow type]" => {
                        quest.grow_type = self.next_int();
                    }
                    "[level]" => {
                        quest.level = self.parse_until_segment_as_int_list();
                    }
                    "[type]" => {
                        quest.quest_type = self.next_str();
                    }
                    "[reward type]" => {
                        quest.reward_type = self.next_str();
                    }
                    "[depend message]" => {
                        quest.depend_message = self.next_str();
                    }
                    "[condition message]" => {
                        quest.condition_message = self.next_str();
                    }
                    "[solve message]" => {
                        quest.solve_message = self.next_str();
                    }
                    "[quest point]" => {
                        quest.quest_point = self.next_int();
                    }
                    "[dungeon info]" => {
                        quest.dungeon_info = self.parse_until_segment_as_int_list();
                    }
                    "[relation quest]" => {
                        quest.relation_quest = self.parse_until_segment_as_int_list();
                    }
                    "[int data]" => {
                        quest.int_data = self.parse_until_segment_as_int_list();
                    }
                    _ => {
                        debug!("skip {:?} in parse quest", segment);
                    }
                }
            }
            self.idx += 1;
        }

        quest
    }
}
