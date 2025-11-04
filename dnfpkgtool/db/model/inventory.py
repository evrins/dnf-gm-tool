from sqlalchemy import BLOB, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    charac_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    money: Mapped[int] = mapped_column(Integer)
    coin: Mapped[int] = mapped_column(Integer)
    inventory: Mapped[bytes] = mapped_column(BLOB)
    equipment_slot: Mapped[bytes] = mapped_column('equipslot', BLOB)
    pay_coin: Mapped[int] = mapped_column(Integer)
    event_coin: Mapped[int] = mapped_column(Integer)
    creature: Mapped[bytes] = mapped_column(BLOB)
    creature_flag: Mapped[int] = mapped_column(Integer)
    katagaki: Mapped[bytes] = mapped_column(BLOB)
    inventory_capacity: Mapped[int] = mapped_column(Integer)
    avatar_coin: Mapped[int] = mapped_column(Integer)
