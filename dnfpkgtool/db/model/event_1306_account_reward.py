import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class Event1306AccountReward(Base):
    __tablename__ = 'event_1306_account_reward'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charac_no: Mapped[int] = mapped_column(Integer)
    occ_date: Mapped[datetime.datetime] = mapped_column(DateTime)
