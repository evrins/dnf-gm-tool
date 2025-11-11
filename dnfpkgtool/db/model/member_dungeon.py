from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class MemberDungeon(Base):
    __tablename__ = 'member_dungeon'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon: Mapped[str] = mapped_column(String)
