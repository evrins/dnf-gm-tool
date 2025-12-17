from sqlalchemy import select
from sqlalchemy.orm import Session

from dnf_db.model.accounts import Accounts
from dnf_db.repo.base_repo import BaseRepo


class AccountsRepo(BaseRepo):
    def __init__(self):
        super().__init__('d_taiwan')

    def query_all(self):
        with Session(self.get_engine()) as session:
            stmt = select(Accounts)
            return session.scalars(stmt).all()
