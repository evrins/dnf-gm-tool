from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class Skill(Base):
    __tablename__ = 'skill'

    charac_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    remain_sp: Mapped[int] = mapped_column(Integer)
    remain_sp_2nd: Mapped[int] = mapped_column(Integer)
    remain_sfp_1st: Mapped[int] = mapped_column(Integer)
    remain_sfp_2nd: Mapped[int] = mapped_column(Integer)
