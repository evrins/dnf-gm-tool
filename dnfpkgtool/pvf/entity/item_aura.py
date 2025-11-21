from pydantic import BaseModel


class ItemAura(BaseModel):
    aura_type: str = ''
    op: str = ''
    num: int = 0
    distance: int = 0
