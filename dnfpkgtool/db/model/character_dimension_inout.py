from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterDimensionInout(Base):
    __tablename__ = 'charac_dimension_inout'

    character_no: Mapped[int] = mapped_column('charac_no', Integer, primary_key=True)
    dungeon1: Mapped[int] = mapped_column(Integer)
    dungeon2: Mapped[int] = mapped_column(Integer)
    dungeon3: Mapped[int] = mapped_column(Integer)
    dungeon4: Mapped[int] = mapped_column(Integer)
    dungeon5: Mapped[int] = mapped_column(Integer)
    dungeon6: Mapped[int] = mapped_column(Integer)
    dungeon7: Mapped[int] = mapped_column(Integer)
    dungeon8: Mapped[int] = mapped_column(Integer)
    dungeon9: Mapped[int] = mapped_column(Integer)
    dungeon10: Mapped[int] = mapped_column(Integer)
