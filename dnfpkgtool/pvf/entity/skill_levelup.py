from pydantic import BaseModel


class SkillLevelUp(BaseModel):
    role: str = ''
    skill_id: int = 0
    level_up: int = 0
