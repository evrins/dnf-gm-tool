from pydantic import BaseModel

from dnfpkgtool.db.entity.mail_form_item import MailItemType


class MailSubmitItem(BaseModel):
    item_type: MailItemType
    item_id: int
    item_name: str

    # 装备最大耐久
    endurance: int = 0

    # 区分 宠物蛋 和 宠物
    sub_type: int = 0
