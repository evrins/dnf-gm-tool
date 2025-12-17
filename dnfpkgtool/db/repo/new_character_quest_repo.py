from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.new_character_quest import NewCharacterQuest
from dnfpkgtool.db.repo.base_repo import BaseRepo


class NewCharacterQuestRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_by_character_no(self, character_no: int) -> NewCharacterQuest:
        with Session(self.get_engine()) as session:
            stmt = (
                select(NewCharacterQuest)
                .where(NewCharacterQuest.charac_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def completed_all_quest_by_character_no(
            self, character_no: int, updates: dict[str, int]
    ):
        with Session(self.get_engine()) as session:
            stmt = (
                update(NewCharacterQuest)
                .where(NewCharacterQuest.charac_no == character_no)
                .values(updates)
            )
            session.execute(stmt)
            session.commit()

    def complete_quest_by_character_no_and_idx(self, character_no: int, idx: int):
        """
        :param character_no:
        :param idx: 1 based index start from 1
        :return:
        """
        with Session(self.get_engine()) as session:
            stmt = (
                update(NewCharacterQuest)
                .where(NewCharacterQuest.charac_no == character_no)
                .values({f'play_{idx}_trigger': 0})
            )
            session.execute(stmt)
            session.commit()

    def cancel_all_quest_by_character_no(self, character_no: int):
        updates = {}
        for i in range(1, 21):
            updates[f'play_{i}'] = 0
            updates[f'play_{i}_trigger'] = 0

        with Session(self.get_engine()) as session:
            stmt = (
                update(NewCharacterQuest)
                .where(NewCharacterQuest.charac_no == character_no)
                .values(updates)
            )
            session.execute(stmt)
            session.commit()

    def cancel_quest_by_character_no_and_idx(self, character_no: int, idx: int):
        """
        :param character_no:
        :param idx: 1 based index start from 1
        :return:
        """
        with Session(self.get_engine()) as session:
            stmt = (
                update(NewCharacterQuest)
                .where(NewCharacterQuest.charac_no == character_no)
                .values({f'play_{idx}': 0, f'play_{idx}_trigger': 0})
            )
            session.execute(stmt)
            session.commit()
