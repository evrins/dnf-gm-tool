from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_info import CharacterInfo
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterInfoRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_all_character_info_list(self) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo)
            return list(session.scalars(stmt).all())

    def query_all_valid_character_info_list(self) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo).where(CharacterInfo.delete_flag == 0)
            return list(session.scalars(stmt).all())

    def query_by_character_no_list(self, character_no_list) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo).where(
                CharacterInfo.character_no.in_(character_no_list)
            )
            return list(session.scalars(stmt).all())

    def query_by_name(self, name: str) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterInfo)
                .where(CharacterInfo.character_name.ilike(f'%{name}%'))
                .order_by(CharacterInfo.character_no.desc())
            )
            return list(session.scalars(stmt).all())

    def query_by_character_no(self, character_no: int) -> CharacterInfo:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterInfo).where(CharacterInfo.character_no == character_no)
            ).limit(1)
            return session.scalars(stmt).first()

    def update_character_info(self, character_info: CharacterInfo):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterInfo)
                .where(CharacterInfo.character_no == character_info.character_no)
                .values(
                    lev=character_info.lev,
                    job=character_info.job,
                    grow_type=character_info.grow_type,
                )
            )
            session.execute(stmt)
            session.commit()


def get_character_info_repo() -> CharacterInfoRepo:
    return CharacterInfoRepo()
