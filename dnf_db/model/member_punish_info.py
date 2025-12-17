from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnf_db.model import Base


class MemberPunishInfo(Base):
    __tablename__ = 'member_punish_info'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
