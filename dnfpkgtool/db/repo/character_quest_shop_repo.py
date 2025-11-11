from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_quest_shop import CharacterQuestShop
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterQuestShopRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_by_character_no(self, character_no: int) -> CharacterQuestShop:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterQuestShop)
                .where(CharacterQuestShop.charac_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def query_qp_by_character_no(self, character_no: int) -> int:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterQuestShop.qp)
                .where(CharacterQuestShop.charac_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def charge(self, it: CharacterQuestShop):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterQuestShop)
                .where(CharacterQuestShop.charac_no == it.charac_no)
                .values(
                    qp=CharacterQuestShop.qp + it.qp,
                )
            )
            session.execute(stmt)
            session.commit()

    def clear_qp_by_character_no(self, character_no: int):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterQuestShop)
                .where(CharacterQuestShop.charac_no == character_no)
                .values(
                    qp=0,
                )
            )
            session.execute(stmt)
            session.commit()


def get_character_quest_shop_repo() -> CharacterQuestShopRepo:
    return CharacterQuestShopRepo()
