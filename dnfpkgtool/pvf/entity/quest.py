from typing import List

from pydantic import BaseModel


class Quest(BaseModel):
    id: int = 0
    grade: str = ''
    difficulty: str = ''
    gold_multiple: int = 0
    npc_index: int = 0
    complete_npc_index: int = 0
    job: str = ''
    grow_type: int = 0
    level: List[int] = []
    quest_type: str = ''
    sub_type: int = 0
    int_data: List[int] = []
    reward_type: str = ''
    name: str = ''
    depend_message: str = ''
    condition_message: str = ''
    solve_message: str = ''
    quest_point: int = 0
    dungeon_info: List[int] = []
    relation_quest: List[int] = []
