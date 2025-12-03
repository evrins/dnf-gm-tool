from pydantic import BaseModel


class SkillLevelUp(BaseModel):
    role: str | None = None
    skill_id: int | None = None
    level_up: int | None = None
