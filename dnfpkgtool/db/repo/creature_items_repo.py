from sqlalchemy import delete
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.creature_items import CreatureItems
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CreatureItemsRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def add(self, ci: CreatureItems) -> CreatureItems:
        with Session(self.get_engine()) as session:
            session.add(ci)
            session.commit()
            session.refresh(ci)
            return ci

    def delete_by_id(self, id_: int):
        with Session(self.get_engine()) as session:
            stmt = delete(CreatureItems).where(CreatureItems.ui_id == id_)
            session.execute(stmt)
            session.commit()


def get_creature_items_repo() -> CreatureItemsRepo:
    return CreatureItemsRepo()
