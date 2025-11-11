from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterQuestShop(Base):
    __tablename__ = 'charac_quest_shop'

    charac_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    qp: Mapped[int] = mapped_column(Integer)
