from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from dnfpkgtool.db.model import Base


class Accounts(Base):
    __tablename__ = 'accounts'

    uid: Mapped[int] = mapped_column('UID', Integer, primary_key=True)
    account_name: Mapped[int] = mapped_column('accountname', Integer)
    password: Mapped[str] = mapped_column(String(128))
    qq: Mapped[str] = mapped_column(String(128))
    dzuid: Mapped[int] = mapped_column(Integer)
    billing: Mapped[int] = mapped_column(Integer)
    vip: Mapped[str] = mapped_column('VIP', String(255))
