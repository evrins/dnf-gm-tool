from typing import List

from pydantic import BaseModel

from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot


class CharacterInventory(BaseModel):
    equipments: List[DnfItemSlot] = []
    creatures: List[DnfItemSlot] = []
    backpack: List[DnfItemSlot] = []
