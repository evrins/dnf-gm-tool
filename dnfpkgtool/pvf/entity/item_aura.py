from pydantic import BaseModel


class ItemAura(BaseModel):
    aura_type: str | None = None
    op: str | None = None
    num: int | None = None
    distance: int | None = None
