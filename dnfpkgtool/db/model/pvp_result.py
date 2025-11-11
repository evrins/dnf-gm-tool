from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class PVPResult(Base):
    __tablename__ = 'pvp_result'

    charac_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    pvp_grade: Mapped[int] = mapped_column(Integer)
    win: Mapped[int] = mapped_column(Integer)
    win_point: Mapped[int] = mapped_column(Integer)
    pvp_point: Mapped[int] = mapped_column(Integer)
