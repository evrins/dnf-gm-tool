from functools import cache
from typing import List, Tuple

from config import config
from dnfpkgtool.db.entity.mail_form_item import MailFormItem, MailItemType
from dnfpkgtool.db.entity.mail_list_item import MailListItem
from dnfpkgtool.db.model.creature_items import CreatureItems
from dnfpkgtool.db.model.letter import Letter
from dnfpkgtool.db.model.postal import Postal
from dnfpkgtool.db.model.user_items import UserItems
from dnfpkgtool.db.repo.creature_items_repo import get_creature_items_repo
from dnfpkgtool.db.repo.letter_repo import get_letter_repo
from dnfpkgtool.db.repo.postal_repo import get_postal_repo
from dnfpkgtool.db.repo.user_items_repo import get_user_items_repo
from dnfpkgtool.repo.equipment_repo import (
    EquipmentIdNotFoundException,
)
from dnfpkgtool.repo.repo_manager import get_equipment_repo, get_stackable_repo
from dnfpkgtool.repo.stackable_repo import (
    StackableIdNotFoundException,
)


class MailService:
    def __init__(self):
        self.letter_repo = get_letter_repo()
        self.postal_repo = get_postal_repo()
        self.user_items_repo = get_user_items_repo()
        self.creature_items_repo = get_creature_items_repo()

        self.stackable_repo = get_stackable_repo()
        self.equipment_repo = get_equipment_repo()

    def get_all_by_character_no(self, character_no: int) -> List[MailListItem]:
        postal_list = self.postal_repo.query_by_character_no(character_no)
        res = []
        for it in postal_list:
            item_name, item_type = self.get_item_name_by_item_id(it.item_id)
            if it.avatar_flag == 1:
                item_type = MailItemType.Avatar
            elif it.creature_flag == 1:
                item_type = MailItemType.Creature
            if item_type == MailItemType.Stackable:
                num = it.add_info
            else:
                num = 1

            mli = MailListItem(
                postal_id=it.postal_id,
                item_name=item_name,
                sender_name=it.send_character_name,
                num=num,
                item_id=it.item_id,
                item_type=item_type,
                add_info=it.add_info,
            )

            res.append(mli)

        return res

    def delete_all(self):
        item_list = self.postal_repo.query_all()
        for it in item_list:
            self.delete_by_postal(it)

    @cache
    def get_item_name_by_item_id(self, item_id: int) -> Tuple[str, MailItemType]:
        try:
            item = self.stackable_repo.query_by_id(item_id)
            return item['name'], MailItemType.Stackable
        except StackableIdNotFoundException:
            pass

        try:
            item = self.equipment_repo.query_by_id(item_id)
            return item['name'], MailItemType.Equipment
        except EquipmentIdNotFoundException:
            pass

        return '未找到', MailItemType.Missing

    def delete_by_mail_list_item(self, mail_list_item: MailListItem):
        if mail_list_item.item_type == MailItemType.Avatar:
            self.user_items_repo.delete_by_id(mail_list_item.add_info)
        elif mail_list_item.item_type == MailItemType.Creature:
            self.creature_items_repo.delete_by_id(mail_list_item.add_info)

        self.postal_repo.delete_by_id(mail_list_item.postal_id)

    # 删除邮件时 需要同时删除附加的 user_items 和 creature_items
    def delete_by_postal_id(self, postal_id: int):
        postal = self.postal_repo.query_by_id(postal_id)
        self.delete_by_postal(postal)

    def delete_by_postal(self, postal: Postal):
        if postal.avatar_flag == 1:
            self.user_items_repo.delete_by_id(postal.item_id)
        elif postal.creature_flag == 1:
            self.creature_items_repo.delete_by_id(postal.item_id)
        self.postal_repo.delete_by_id(postal.postal_id)

    def send_mail(
        self, sender: str, msg: str, character_no: int, mail_item: MailFormItem
    ):
        if mail_item.item_type == MailItemType.Stackable:
            self.send_stackable_mail(sender, msg, character_no, mail_item)
        elif mail_item.item_type == MailItemType.Creature:
            self.send_creature_mail(sender, msg, character_no, mail_item)
        elif mail_item.item_type == MailItemType.Equipment:
            self.send_equipment_mail(sender, msg, character_no, mail_item)
        elif mail_item.item_type == MailItemType.Avatar:
            self.send_avatar_mail(sender, msg, character_no, mail_item)

    def send_letter(self, sender: str, msg: str, character_no: int) -> Letter:
        letter = Letter.default()
        letter.character_no = character_no
        letter.send_character_name = sender
        letter.letter_text = msg
        return self.letter_repo.add(letter)

    def send_creature_mail(
        self, sender: str, msg: str, character_no: int, mail_item: MailFormItem
    ):
        letter = self.send_letter(sender, msg, character_no)

        creature = CreatureItems.default()
        creature.character_no = character_no
        creature.it_id = mail_item.item_id
        # 不知道为什么和 pvf 定义中的 sub_type 值是反的
        creature.creature_type = 0 if mail_item.sub_type == 1 else 1

        creature = self.creature_items_repo.add(creature)

        it = Postal.default()
        it.send_character_name = sender
        it.receive_character_no = character_no
        it.item_id = mail_item.item_id
        it.letter_id = letter.letter_id
        it.gold = mail_item.gold
        it.creature_flag = 1

        it.add_info = creature.ui_id

        self.postal_repo.add(it)

    def send_avatar_mail(
        self, sender: str, msg: str, character_no: int, mail_item: MailFormItem
    ):
        avatar = UserItems.default()
        avatar.character_no = character_no
        avatar.it_id = mail_item.item_id
        avatar = self.user_items_repo.add(avatar)

        letter = self.send_letter(sender, msg, character_no)
        it = Postal.default()
        it.send_character_name = sender
        it.receive_character_no = character_no
        it.item_id = mail_item.item_id
        it.letter_id = letter.letter_id
        it.gold = mail_item.gold
        it.avatar_flag = 1

        it.add_info = avatar.ui_id

        self.postal_repo.add(it)

    def send_equipment_mail(
        self, sender: str, msg: str, character_no: int, mail_item: MailFormItem
    ):
        letter = self.send_letter(sender, msg, character_no)
        it = Postal.default()
        it.send_character_name = sender
        it.receive_character_no = character_no
        it.item_id = mail_item.item_id
        it.add_info = mail_item.grade
        it.letter_id = letter.letter_id
        it.gold = mail_item.gold

        it.amplify_option = mail_item.amplify_option
        it.amplify_value = mail_item.amplify_value
        it.separate_upgrade = mail_item.separate_upgrade
        it.seal_flag = mail_item.seal_flag
        it.upgrade = mail_item.upgrade
        it.endurance = mail_item.endurance

        self.postal_repo.add(it)

    # 发送可堆叠物品
    def send_stackable_mail(
        self, sender: str, msg: str, character_no: int, mail_item: MailFormItem
    ):
        # 每封邮件可以有 8 个附件, 对于超过可堆叠上限的物品, 每 8 条 postal 记录, 重新插入一条 letter 记录
        item = self.stackable_repo.query_by_id(mail_item.item_id)
        stack_limit = item['stack_limit']
        if stack_limit == 0:
            stack_limit = 1_000_000

        batch_size, reminder = divmod(mail_item.num, stack_limit)

        for i in range(batch_size + 1):
            if i % 8 == 0:
                letter = self.send_letter(sender, msg, character_no)

            item_count = stack_limit if i < batch_size else reminder
            it = Postal.default()
            it.send_character_name = sender
            it.receive_character_no = character_no
            it.item_id = mail_item.item_id
            it.add_info = item_count
            it.letter_id = letter.letter_id
            it.gold = mail_item.gold
            self.postal_repo.add(it)

            # 只有第一封邮件有金币 后面的都没有
            mail_item.gold = 0

    def get_current_character_postal(self) -> List[MailListItem]:
        character_no = config.get_current_character_no()
        return self.get_all_by_character_no(character_no)

    def send_current_character_mail(
        self, sender: str, msg: str, mail_item: MailFormItem
    ):
        character_no = config.get_current_character_no()
        self.send_mail(sender, msg, character_no, mail_item)
