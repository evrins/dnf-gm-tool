from pydantic import BaseModel

from dnf_db.entity.mail_form_item import MailItemType


class MailSubmitItem(BaseModel):
    item_type: MailItemType
    item_id: int
    item_name: str

    # 可堆叠物品最大叠放数
    stack_limit: int = 0

    # 装备最大耐久
    endurance: int = 0

    # 区分 宠物蛋 和 宠物
    sub_type: int = 0
