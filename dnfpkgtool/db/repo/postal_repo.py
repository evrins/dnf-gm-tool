from typing import List

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.postal import Postal
from dnfpkgtool.db.repo.base_repo import BaseRepo


class PostalRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def add(self, it: Postal) -> Postal:
        with Session(self.get_engine()) as session:
            session.add(it)
            session.commit()
            return it

    def query_by_character_no(self, character_no: int) -> List[Postal]:
        with Session(self.get_engine()) as session:
            stmt = (
                select(Postal)
                .filter(Postal.receive_character_no == character_no)
                .filter(Postal.delete_flag == 0)
                .filter(Postal.item_id != 0)
            )
            return session.scalars(stmt).all()

    def query_by_id(self, id_: int) -> Postal:
        with Session(self.get_engine()) as session:
            stmt = select(Postal).where(Postal.postal_id == id_)
            return session.scalars(stmt).first()

    def delete_by_id(self, id_: int) -> bool:
        """Delete a postal item by ID. Returns True if deletion was successful."""
        with Session(self.get_engine()) as session:
            stmt = delete(Postal).where(Postal.postal_id == id_)
            result = session.execute(stmt)
            session.commit()  # Commit the transaction to persist changes
            return result.rowcount > 0  # Return True if at least one row was deleted

    def query_all(self) -> List[Postal]:
        with Session(self.get_engine()) as session:
            stmt = select(Postal)
            return session.scalars(stmt).all()


def get_postal_repo() -> PostalRepo:
    return PostalRepo()
