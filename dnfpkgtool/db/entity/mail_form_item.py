from enum import Enum

from pydantic import BaseModel


class ItemType(Enum):
    Stackable = 1
    Equipment = 2
    Avatar = 3
    Creature = 4

    def __repr__(self):
        if self == self.Stackable:
            return '道具'
        elif self == self.Equipment:
            return '装备'
        elif self == self.Avatar:
            return '时装'
        elif self == self.Creature:
            return '宠物'
        return None

    __str__ = __repr__


class MailFormItem(BaseModel):
    item_type: ItemType
    item_id: int
    gold: int = 0

    # 可堆叠物品独有
    num: int = 0

    # 装备独有
    # 品级
    grade: int = 0
    amplify_option: int = 0
    amplify_value: int = 0
    separate_upgrade: int = 0
    seal_flag: int = 0
    upgrade: int = 0
    endurance: int = 0

    # 区分 宠物蛋 和 宠物
    sub_type: int = 0
