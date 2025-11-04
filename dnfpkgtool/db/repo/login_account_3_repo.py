from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.login_account_3 import LoginAccount3
from dnfpkgtool.db.repo.base_repo import BaseRepo


class LoginAccount3Repo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_login')

    def query_logged_account_m_id(self) -> List[int]:
        with Session(self.get_engine()) as session:
            stmt = select(LoginAccount3.m_id).where(LoginAccount3.login_status)
            return list(session.scalars(stmt).all())
