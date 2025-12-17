from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnf_db.model.cash_cera import CashCera
from dnf_db.repo.base_repo import BaseRepo


class CashCeraRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_billing')

    def query_cera_by_account(self, m_id: str) -> int:
        with Session(self.get_engine()) as session:
            stmt = select(CashCera.cera).where(CashCera.account == m_id).limit(1)
            return session.scalars(stmt).first()

    def charge_cera(self, it: CashCera):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CashCera)
                .where(CashCera.account == it.account)
                .values(
                    cera=CashCera.cera + it.cera,
                )
            )
            session.execute(stmt)
            session.commit()

    def clear_cera_by_account(self, account: str):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CashCera)
                .where(CashCera.account == account)
                .values(
                    cera=0,
                )
            )
            session.execute(stmt)
            session.commit()


def get_cash_cera_repo() -> CashCeraRepo:
    return CashCeraRepo()
