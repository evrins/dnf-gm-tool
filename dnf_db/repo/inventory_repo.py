from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnf_db.model.inventory import Inventory
from dnf_db.repo.base_repo import BaseRepo


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

    def query_money_by_character_no(self, character_no: int) -> int:
        with Session(self.get_engine()) as session:
            stmt = (
                select(Inventory.money)
                .where(Inventory.charac_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def update_money_by_character_no(self, character_no: int, new_money: int) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(Inventory)
                .where(Inventory.charac_no == character_no)
                .values(money=new_money)
            )
            session.execute(stmt)
            session.commit()

    def query_pay_coin_by_character_no(self, character_no: int) -> int:
        with Session(self.get_engine()) as session:
            stmt = (
                select(Inventory.pay_coin)
                .where(Inventory.charac_no == character_no)
                .limit(1)
            )
            return session.scalars(stmt).first()

    def update_pay_coin_by_character_no(self, character_no: int, pay_coin: int) -> None:
        with Session(self.get_engine()) as session:
            stmt = (
                update(Inventory)
                .where(Inventory.charac_no == character_no)
                .values(pay_coin=pay_coin)
            )
            session.execute(stmt)
            session.commit()


def get_inventory_repo() -> InventoryRepo:
    return InventoryRepo()
