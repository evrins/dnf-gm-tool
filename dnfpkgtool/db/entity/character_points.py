from pydantic import BaseModel


class CharacterPoints(BaseModel):
    cash_cera: int = 0
    cash_cera_point: int = 0
    skill_point: int = 0
    quest_point: int = 0
    tp: int = 0
