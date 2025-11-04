from sqlalchemy import BLOB, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterInventoryExpand(Base):
    __tablename__ = 'charac_inven_expand'

    charac_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    cargo: Mapped[bytes] = mapped_column(BLOB)
    cargo_capacity: Mapped[int] = mapped_column(Integer)
    jewel: Mapped[bytes] = mapped_column(BLOB)
    current_equipment_slot: Mapped[bytes] = mapped_column('current_equipslot', BLOB)
    switch_equipment_slot: Mapped[bytes] = mapped_column('switch_equipslot', BLOB)
    expand_equipment_slot: Mapped[bytes] = mapped_column('expand_equipslot', BLOB)
    redeem_info: Mapped[bytes] = mapped_column(BLOB)
