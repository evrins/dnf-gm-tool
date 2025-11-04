import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from dnfpkgtool.db.model import Base


class LoginAccount3(Base):
    __tablename__ = 'login_account_3'

    m_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    m_channel_no: Mapped[int] = mapped_column(Integer)
    login_status: Mapped[bool] = mapped_column(TINYINT)
    last_login_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    login_ip: Mapped[str] = mapped_column(VARCHAR)
