from typing import List

from loguru import logger
from pydantic import BaseModel

from config import config
from dnfpkgtool.db.entity.mail_form_item import MailFormItem, MailItemType
from dnfpkgtool.db.repo.new_character_quest_repo import NewCharacterQuestRepo
from dnfpkgtool.db.service.item_service import ItemService, ItemType
from dnfpkgtool.db.service.mail_service import MailService
from dnfpkgtool.repo.repo_manager import get_quest_repo


class CharacterQuest(BaseModel):
    quest_list: List[Quest]


class Quest(BaseModel):
    idx: int
    id: int
    name: str = ''
    status: int
    type_: str = ''
    detail: str = ''
    required_items: List[int] = []


class QuestService:
    def __init__(self):
        self.character_quest_repo = NewCharacterQuestRepo()
        self.quest_repo = get_quest_repo()

        self.item_service = ItemService()
        self.mail_service = MailService()

    def get_current_character_quest(self) -> CharacterQuest:
        character_no = config.get_current_character_no()
        return self.get_quest_by_character_no(character_no)

    def get_quest_by_character_no(self, character_no: int) -> CharacterQuest:
        entity = self.character_quest_repo.query_by_character_no(character_no)
        quest_list: List[Quest] = []
        for i in range(1, 21):
            id_key = f'play_{i}'
            status_key = f'play_{i}_trigger'
            id_ = getattr(entity, id_key)
            status = getattr(entity, status_key)
            q = Quest(
                idx=i,
                id=id_,
                status=status,
            )
            if q.id != 0:
                quest_meta = self.quest_repo.query_by_id(id_)
                q.name = quest_meta['name']
                q.type_ = quest_meta['quest_type']
                q.required_items = quest_meta['int_data']
                q.detail = quest_meta['json']
            quest_list.append(q)
        cq = CharacterQuest(quest_list=quest_list)
        return cq

    def complete_current_character_quest(self, q: Quest):
        current_character_no = config.get_current_character_no()
        self.complete_quest(current_character_no, q)

    def complete_quest(self, character_no: int, q: Quest):
        if q.id == 0:
            return

        if q.type_ == '[seeking]':
            self.send_quest_item(character_no, q)
        else:
            self.character_quest_repo.complete_quest_by_character_no_and_idx(
                character_no, q.idx
            )

    def complete_current_character_all_quests(self, cq: CharacterQuest):
        current_character_no = config.get_current_character_no()
        self.complete_all_quests(current_character_no, cq)

    def complete_all_quests(self, character_no: int, cq: CharacterQuest):
        updates = {}
        for i, q in enumerate(cq.quest_list):
            if q.id == 0:
                continue
            if q.type_ == '[seeking]':
                self.send_quest_item(character_no, q)
            else:
                updates[f'play_{i + 1}_trigger'] = 0
        self.character_quest_repo.completed_all_quest_by_character_no(
            character_no, updates
        )

    def send_quest_item(self, character_no: int, q: Quest):
        n = len(q.required_items)
        for i in range(0, n, 2):
            item_id = q.required_items[i]
            num = q.required_items[i + 1]
            try:
                item_type, item = self.item_service.find_by_id(item_id)
                if item_type == ItemType.Stackable:
                    mail_item = MailFormItem(
                        item_type=MailItemType.Stackable,
                        item_id=item_id,
                        num=num,
                    )
                    self.mail_service.send_mail(
                        'hello', 'world', character_no, mail_item
                    )
                elif item_type == ItemType.Equipment:
                    mail_item = MailFormItem(
                        item_type=MailItemType.Equipment,
                        item_id=item_id,
                        num=num,
                        endurance=item['durability'],
                    )
                    self.mail_service.send_mail(
                        'hello', 'world', character_no, mail_item
                    )

            except Exception as e:
                logger.error(f'Failed to find item {item_id}, {e}')

    def cancel_current_character_all_quests(self):
        current_character_no = config.get_current_character_no()
        self.cancel_all_quests(current_character_no)

    def cancel_all_quests(self, character_no: int):
        self.character_quest_repo.cancel_all_quest_by_character_no(character_no)

    def cancel_current_character_quest_by_idx(self, idx: int):
        current_character_no = config.get_current_character_no()
        self.cancel_quest_by_idx(current_character_no, idx)

    def cancel_quest_by_idx(self, character_no: int, idx: int):
        self.character_quest_repo.cancel_quest_by_character_no_and_idx(
            character_no, idx
        )
