from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnf_db.model import Base


class CharacterBloodDungeonReward(Base):
    __tablename__ = 'charac_blood_dungeon_reward'

    character_no: Mapped[int] = mapped_column('charac_no', Integer, primary_key=True)
    enter_count: Mapped[int] = mapped_column(Integer)
