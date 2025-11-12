from sqlalchemy import delete
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.member_punish_info import MemberPunishInfo
from dnfpkgtool.db.repo.base_repo import BaseRepo


class MemberPunishInfoRepo(BaseRepo):
    def __init__(self):
        super().__init__('d_taiwan')

    def delete_by_m_id(self, m_id: int):
        with Session(self.get_engine()) as session:
            stmt = delete(MemberPunishInfo).where(MemberPunishInfo.m_id == m_id)
            session.execute(stmt)
            session.commit()


def get_member_punish_info_repo() -> MemberPunishInfoRepo:
    return MemberPunishInfoRepo()
