from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.pvp_result import PVPResult
from dnfpkgtool.db.repo.base_repo import BaseRepo


class PVPResultRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_by_character_no(self, character_no: int) -> PVPResult:
        with Session(self.get_engine()) as session:
            stmt = select(PVPResult).where(PVPResult.charac_no == character_no).limit(1)
            return session.scalars(stmt).first()

    def update(self, it: PVPResult):
        with Session(self.get_engine()) as session:
            stmt = (
                update(PVPResult)
                .where(PVPResult.charac_no == it.charac_no)
                .values(
                    pvp_grade=it.pvp_grade,
                    win=it.win,
                    win_point=it.win_point,
                    pvp_point=it.pvp_point,
                )
            )
            session.execute(stmt)
            session.commit()


def get_pvp_result_repo() -> PVPResultRepo:
    return PVPResultRepo()
