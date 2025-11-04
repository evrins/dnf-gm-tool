from pydantic import BaseModel

from dnfpkgtool.db.entity.mail_form_item import ItemType


class MailSubmitItem(BaseModel):
    item_type: ItemType
    item_id: int
    item_name: str

    # 装备最大耐久
    endurance: int = 0

    # 区分 宠物蛋 和 宠物
    sub_type: int = 0
