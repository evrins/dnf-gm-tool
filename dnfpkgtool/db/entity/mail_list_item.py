from pydantic import BaseModel

from dnfpkgtool.db.entity.mail_form_item import ItemType


class MailListItem(BaseModel):
    postal_id: int = 0

    sender_name: str = ''
    item_id: int = 0
    item_name: str = ''
    item_type: ItemType

    num: int = 0

    # UserItems.ui_id 或者 CreatureItems.ui_id
    add_info: int = 0
