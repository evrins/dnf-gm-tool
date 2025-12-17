from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnf_db.model import Base


class LimitCreateCharacter(Base):
    __tablename__ = 'limit_create_character'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
