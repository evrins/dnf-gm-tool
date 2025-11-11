from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class CharacterInfo(Base):
    __tablename__ = 'charac_info'

    m_id: Mapped[int] = mapped_column(Integer)
    character_no: Mapped[int] = mapped_column('charac_no', Integer, primary_key=True)
    character_name: Mapped[str] = mapped_column('charac_name', String(20))
    lev: Mapped[int] = mapped_column(Integer)
    job: Mapped[int] = mapped_column(Integer)
    grow_type: Mapped[int] = mapped_column(Integer)
    delete_flag: Mapped[int] = mapped_column(Integer)
    expert_job: Mapped[int] = mapped_column(Integer)
