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
                        quest.name = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[difficulty]" => {
                        quest.difficulty = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[gold multiple]" => {
                        quest.gold_multiple = *self.parse_next_one().as_int().unwrap();
                    }
                    "[npc index]" => {
                        quest.npc_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[complete npc index]" => {
                        quest.complete_npc_index = *self.parse_next_one().as_int().unwrap();
                    }
                    "[job]" => {
                        quest.job = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[grow type]" => {
                        quest.grow_type = *self.parse_next_one().as_int().unwrap();
                    }
                    "[level]" => {
                        quest.level = self.parse_until_segment_as_int_list();
                    }
                    "[type]" => {
                        quest.quest_type = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[reward type]" => {
                        quest.reward_type = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[depend message]" => {
                        quest.depend_message = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[condition message]" => {
                        quest.condition_message =
                            self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[solve message]" => {
                        quest.solve_message = self.parse_next_one().as_string().unwrap().clone();
                    }
                    "[quest point]" => {
                        quest.quest_point = *self.parse_next_one().as_int().unwrap();
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
