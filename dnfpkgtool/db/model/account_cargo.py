import datetime

from sqlalchemy import BLOB, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class AccountCargo(Base):
    __tablename__ = 'account_cargo'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    money: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)
    cargo: Mapped[bytes] = mapped_column(BLOB)
    occ_time: Mapped[datetime.datetime] = mapped_column(DateTime)
