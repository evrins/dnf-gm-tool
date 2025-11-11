from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.cash_cera_point import CashCeraPoint
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CashCeraPointRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_billing')

    def query_cera_point_by_account(self, m_id: str) -> int:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CashCeraPoint.cera_point)
                .where(CashCeraPoint.account == m_id)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def charge_cera_point(self, it: CashCeraPoint):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CashCeraPoint)
                .where(CashCeraPoint.account == it.account)
                .values(
                    cera_point=CashCeraPoint.cera_point + it.cera_point,
                )
            )
            session.execute(stmt)
            session.commit()

    def clear_cera_point_by_account(self, account: str):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CashCeraPoint)
                .where(CashCeraPoint.account == account)
                .values(
                    cera_point=0,
                )
            )
            session.execute(stmt)
            session.commit()


def get_cash_cera_point_repo() -> CashCeraPointRepo:
    return CashCeraPointRepo()
