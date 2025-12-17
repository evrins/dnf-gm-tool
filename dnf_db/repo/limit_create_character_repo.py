from sqlalchemy import update
from sqlalchemy.orm import Session

from dnf_db.model.limit_create_character import LimitCreateCharacter
from dnf_db.repo.base_repo import BaseRepo


class LimitCreateCharacterRepo(BaseRepo):
    def __init__(self):
        super().__init__('d_taiwan')

    def update(self, it: LimitCreateCharacter):
        with Session(self.get_engine()) as session:
            stmt = (
                update(LimitCreateCharacter)
                .where(LimitCreateCharacter.m_id == it.m_id)
                .values(
                    count=it.count,
                )
            )
            session.execute(stmt)
            session.commit()


def get_limit_create_character_repo() -> LimitCreateCharacterRepo:
    return LimitCreateCharacterRepo()
