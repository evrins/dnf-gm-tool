from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dnf_db.model import Base


class Postal(Base):
    __tablename__ = 'postal'

    postal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    occ_time: Mapped[datetime] = mapped_column(DateTime)
    send_character_no: Mapped[int] = mapped_column('send_charac_no', Integer)
    send_character_name: Mapped[str] = mapped_column('send_charac_name', String(20))
    receive_character_no: Mapped[int] = mapped_column('receive_charac_no', Integer)
    # 增幅类型
    amplify_option: Mapped[int] = mapped_column(Integer)
    # 增幅值
    amplify_value: Mapped[int] = mapped_column(Integer)
    # 锻造等级
    separate_upgrade: Mapped[int] = mapped_column('seperate_upgrade', Integer)
    # 是否封装
    seal_flag: Mapped[int] = mapped_column(Integer)
    # 物品id
    item_id: Mapped[int] = mapped_column(Integer)
    # 数量 或者 品级 或者 UserItems.ui_id 或者 CreatureItems.ui_id
    add_info: Mapped[int] = mapped_column(Integer)
    # 强化
    upgrade: Mapped[int] = mapped_column(Integer)
    # 金钱
    gold: Mapped[int] = mapped_column(Integer)
    # 关联 letter letter_id
    letter_id: Mapped[int] = mapped_column(Integer)
    # 是否时装
    avatar_flag: Mapped[int] = mapped_column('avata_flag', Integer)
    # 是否宠物
    creature_flag: Mapped[int] = mapped_column(Integer)
    # 耐久
    endurance: Mapped[int] = mapped_column(Integer)
    # ???
    unlimit_flag: Mapped[int] = mapped_column(Integer)
    delete_flag: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def default() -> 'Postal':
        return Postal(
            occ_time=datetime.now(),
            send_character_no=0,
            amplify_option=0,
            amplify_value=0,
            separate_upgrade=0,
            seal_flag=0,
            upgrade=0,
            gold=0,
            avatar_flag=0,
            creature_flag=0,
            endurance=0,
            unlimit_flag=1,
            delete_flag=0,
        )
