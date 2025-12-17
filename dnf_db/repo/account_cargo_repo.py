from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnf_db.model.account_cargo import AccountCargo
from dnf_db.repo.base_repo import BaseRepo


class AccountCargoRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def query_by_m_id(self, m_id: int) -> AccountCargo:
        with Session(self.get_engine()) as session:
            stmt = select(AccountCargo).where(AccountCargo.m_id == m_id)
            return session.scalars(stmt).first()

    def update_cargo_by_m_id(self, m_id: int, new_cargo: bytes):
        with Session(self.get_engine()) as session:
            stmt = (
                update(AccountCargo)
                .where(AccountCargo.m_id == m_id)
                .values(cargo=new_cargo)
            )
            session.execute(stmt)
            session.commit()

    def query_money_by_m_id(self, m_id: int) -> int:
        with Session(self.get_engine()) as session:
            stmt = select(AccountCargo.money).where(AccountCargo.m_id == m_id).limit(1)
            return session.scalars(stmt).first()

    def update_money_by_m_id(self, m_id: int, new_money: int):
        with Session(self.get_engine()) as session:
            stmt = (
                update(AccountCargo)
                .where(AccountCargo.m_id == m_id)
                .values(money=new_money)
            )
            session.execute(stmt)
            session.commit()


def get_account_cargo_repo() -> AccountCargoRepo:
    return AccountCargoRepo()
