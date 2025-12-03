from typing import List

from pydantic import BaseModel


class Emancipate(BaseModel):
    input: List[int] = []
    output: List[int] = []
    emancipate_explain: str = ''
