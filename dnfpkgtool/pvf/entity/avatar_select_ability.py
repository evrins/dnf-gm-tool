from pydantic import BaseModel


class AvatarSelectAbility(BaseModel):
    ability_type: str = ''
    role: str = ''
    skill_id: int = 0
    level_up: int = 0
