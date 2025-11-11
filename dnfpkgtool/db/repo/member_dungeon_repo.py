from sqlalchemy import update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.member_dungeon import MemberDungeon
from dnfpkgtool.db.repo.base_repo import BaseRepo


class MemberDungeonRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def update(self, it: MemberDungeon):
        with Session(self.get_engine()) as session:
            stmt = (
                update(MemberDungeon)
                .where(MemberDungeon.m_id == it.m_id)
                .values(
                    dungeon=it.dungeon,
                )
            )
            session.execute(stmt)
            session.commit()


def get_member_dungeon_repo() -> MemberDungeonRepo:
    return MemberDungeonRepo()
