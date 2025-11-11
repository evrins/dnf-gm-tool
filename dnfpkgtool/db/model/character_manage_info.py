from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterManageInfo(Base):
    __tablename__ = 'charac_manage_info'

    character_no: Mapped[int] = mapped_column('charac_no', Integer, primary_key=True)
    max_equip_level: Mapped[int] = mapped_column(Integer)
