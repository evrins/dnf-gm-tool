from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnf_db.model import Base


class CashCeraPoint(Base):
    __tablename__ = 'cash_cera_point'

    account: Mapped[str] = mapped_column(String(30), primary_key=True)
    cera_point: Mapped[int] = mapped_column(Integer)
