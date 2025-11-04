from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.inventory import Inventory
from dnfpkgtool.db.repo.base_repo import BaseRepo


class InventoryRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def query_by_character_no(self, character_no) -> Inventory:
        with Session(self.get_engine()) as session:
            stmt = select(Inventory).where(Inventory.charac_no == character_no)
            return session.scalars(stmt).first()

    def update_equipments_by_character_no(
        self, character_no: int, equipments: bytes
    ) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(Inventory)
                .where(Inventory.charac_no == character_no)
                .values(equipment_slot=equipments)
            )
            session.execute(stmt)
            session.commit()

    def update_creatures_by_character_no(
        self, character_no: int, creatures: bytes
    ) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(Inventory)
                .where(Inventory.charac_no == character_no)
                .values(creature=creatures)
            )
            session.execute(stmt)
            session.commit()

    def update_inventory_by_character_no(
        self, character_no: int, inventory: bytes
    ) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(Inventory)
                .where(Inventory.charac_no == character_no)
                .values(inventory=inventory)
            )
            session.execute(stmt)
            session.commit()


def get_inventory_repo() -> InventoryRepo:
    return InventoryRepo()
