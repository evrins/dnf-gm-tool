from typing import List

from pydantic import BaseModel

from dnfpkgtool.pvf.entity.piece_set_ability import PieceSetAbility


class PieceSet(BaseModel):
    set_name: str = ''
    piece_set_ability: List[PieceSetAbility] = []
    parameter_basic_explain: str = ''
    part_set_index: int = 0
