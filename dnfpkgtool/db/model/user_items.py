from datetime import datetime, timedelta

from sqlalchemy import BLOB, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class UserItems(Base):
    __tablename__ = 'user_items'

    ui_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_no: Mapped[int] = mapped_column('charac_no', Integer)
    it_id: Mapped[int] = mapped_column(Integer)
    jewel_socket: Mapped[bytes] = mapped_column(BLOB)
    expire_date: Mapped[datetime] = mapped_column(DateTime)
    obtain_from: Mapped[int] = mapped_column(Integer)
    reg_date: Mapped[datetime] = mapped_column(DateTime)
    stat: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def default() -> 'UserItems':
        return UserItems(
            jewel_socket=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            expire_date=datetime.max - timedelta(days=1),
            reg_date=datetime.now(),
            obtain_from=1,
            stat=2,
        )
