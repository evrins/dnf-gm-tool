from typing import List

from pydantic import BaseModel


class SkillApplyCondition(BaseModel):
    skill_group: str = ''
    lower_bound_level: int = 0
    upper_bound_level: int = 0
    value: int = 0
    extra_condition: List[str] = []
