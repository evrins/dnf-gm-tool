from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from dnf_db.model.user_items import UserItems
from dnf_db.repo.base_repo import BaseRepo


class UserItemsRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def add(self, it: UserItems) -> UserItems:
        with Session(self.get_engine()) as session:
            session.add(it)
            session.commit()
            session.refresh(it)
            return it

    def query_by_id(self, id_: int) -> UserItems:
        with Session(self.get_engine()) as session:
            stmt = select(UserItems).where(UserItems.ui_id == id_)
            return session.scalars(stmt).first()

    def delete_by_id(self, id_: int):
        with Session(self.get_engine()) as session:
            stmt = delete(UserItems).where(UserItems.ui_id == id_)
            session.execute(stmt)
            session.commit()


def get_user_items_repo() -> UserItemsRepo:
    return UserItemsRepo()
