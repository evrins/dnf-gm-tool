from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_stat import CharacterStat
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterStatRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_by_character_no(self, character_no: int) -> CharacterStat:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterStat)
                .where(CharacterStat.character_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def update_exp(self, it: CharacterStat):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterStat)
                .where(CharacterStat.character_no == it.character_no)
                .values(
                    exp=it.exp,
                )
            )
            session.execute(stmt)
            session.commit()

    def update_add_slot_flag(self, it: CharacterStat):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterStat)
                .where(CharacterStat.character_no == it.character_no)
                .values(
                    add_slot_flag=it.add_slot_flag,
                )
            )
            session.execute(stmt)
            session.commit()

    def update_expert_level(self, it: CharacterStat):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterStat)
                .where(CharacterStat.character_no == it.character_no)
                .values(
                    expert_job_exp=it.expert_job_exp,
                )
            )
            session.execute(stmt)
            session.commit()


def get_character_stat_repo() -> CharacterStatRepo:
    return CharacterStatRepo()
