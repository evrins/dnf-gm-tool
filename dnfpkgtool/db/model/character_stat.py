from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterStat(Base):
    __tablename__ = 'charac_stat'

    character_no: Mapped[int] = mapped_column('charac_no', Integer, primary_key=True)
    exp: Mapped[int] = mapped_column(Integer)
    fatigue: Mapped[int] = mapped_column(Integer)
    used_fatigue: Mapped[int] = mapped_column(Integer)
    add_slot_flag: Mapped[int] = mapped_column(Integer)
    expert_job_exp: Mapped[int] = mapped_column(Integer)
