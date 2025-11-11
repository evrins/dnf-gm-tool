from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CashCera(Base):
    __tablename__ = 'cash_cera'

    account: Mapped[str] = mapped_column(String(30), primary_key=True)
    cera: Mapped[int] = mapped_column(Integer)
