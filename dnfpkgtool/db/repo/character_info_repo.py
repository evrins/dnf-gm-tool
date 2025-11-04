from typing import List

from sqlalchemy import select
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
                CharacterInfo.charac_no.in_(character_no_list)
            )
            return list(session.scalars(stmt).all())

    def query_by_name(self, name: str) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterInfo)
                .where(CharacterInfo.charac_name.ilike(f'%{name}%'))
                .order_by(CharacterInfo.charac_no.desc())
            )
            return list(session.scalars(stmt).all())
