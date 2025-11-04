from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class Letter(Base):
    __tablename__ = 'letter'

    letter_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_no: Mapped[int] = mapped_column('charac_no', Integer)
    send_character_no: Mapped[int] = mapped_column('send_charac_no', Integer)
    send_character_name: Mapped[str] = mapped_column('send_charac_name', String(20))
    letter_text: Mapped[str] = mapped_column(String(255))
    reg_date: Mapped[datetime] = mapped_column(DateTime)
    stat: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def default() -> 'Letter':
        return Letter(
            send_character_no=0,
            reg_date=datetime.now(),
            stat=1,
        )
