from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_inventory_expand import CharacterInventoryExpand
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterInventoryExpandRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def query_by_character_no(self, character_no) -> CharacterInventoryExpand:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInventoryExpand).where(
                CharacterInventoryExpand.charac_no == character_no
            )
            return session.scalars(stmt).first()

    def update_cargo_by_character_no(self, character_no: int, new_cargo: bytes) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterInventoryExpand)
                .where(CharacterInventoryExpand.charac_no == character_no)
                .values(cargo=new_cargo)
            )
            session.execute(stmt)
            session.commit()


def get_character_inventory_expand_repo() -> CharacterInventoryExpandRepo:
    return CharacterInventoryExpandRepo()
