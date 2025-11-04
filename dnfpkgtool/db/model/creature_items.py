from datetime import datetime, timedelta

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CreatureItems(Base):
    __tablename__ = 'creature_items'

    ui_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_no: Mapped[int] = mapped_column('charac_no', Integer)
    it_id: Mapped[int] = mapped_column(Integer)
    expire_date: Mapped[datetime] = mapped_column(DateTime)
    reg_date: Mapped[datetime] = mapped_column(DateTime)
    stat: Mapped[int] = mapped_column(Integer)
    item_lock_key: Mapped[int] = mapped_column(Integer)
    creature_type: Mapped[int] = mapped_column(Integer)
    # 饱食度
    stomach: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def default() -> 'CreatureItems':
        return CreatureItems(
            expire_date=datetime.max - timedelta(days=1),
            reg_date=datetime.now(),
            stat=0,
            item_lock_key=0,
            stomach=100,
        )
