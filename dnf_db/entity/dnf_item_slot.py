import struct
from typing import List

from pydantic import BaseModel

from dnf_db.entity.magic_seal import MagicSeal

type_dict = {
    0x00: '已删除/空槽位',
    0x01: '装备',
    0x02: '消耗品',
    0x03: '材料',
    0x04: '任务材料',
    0x05: '宠物',
    0x06: '宠物装备',
    0x07: '宠物消耗品',
    0x0A: '副职业',
}

type_dict_rev = {v: k for k, v in type_dict.items()}

reinforce_type_dict = {
    0x00: '空-0',
    0x01: '异次元体力-1',
    0x02: '异次元精神-2',
    0x03: '异次元力量-3',
    0x04: '异次元智力-4',
}


class DnfItemSlot(BaseModel):
    is_sealed: int = False
    type: int = 0
    id: int = 0
    enhancement_level: int = 0
    seal_count: int = 0
    num_grade: int = 0
    endurance: int = 0
    # 虽然附魔使用的是附魔宝珠 但是绑定的是卡片的 id
    card_id: int = 0
    reinforce_type: int = 0
    reinforce_value: int = 0
    _others20_30: bytes = b''
    otherworld: bytes = b''
    _others32_36: bytes = b''
    magic_seal: bytes = b''
    cover_magic_idx: int = 0
    forge_level: int = 0
    _others: bytes = b''

    # item index in bytes
    display_idx: int = 0
    display_type: str = ''
    display_name: str = ''
    display_category: str = ''
    equipment_type: str = ''
    display_reinforce_type: str = ''
    display_rarity: int = 0
    display_rarity_name: str = ''
    display_magic_seals: List[MagicSeal] = [MagicSeal()] * 4
    is_missing: bool = False

    is_equipment: bool = False
    # 装备最大耐久 修改耐久大于该值会报错
    endurance_limit: int = 0
    stack_limit: int = 0

    def __init__(self, buf: bytes):
        super().__init__()

        if len(buf) < 61:
            buf = b'\x00' * 61

        self.is_sealed = buf[0]
        self.type = buf[1]
        self.display_type = type_dict.get(self.type)
        self.id = struct.unpack('I', buf[2:6])[0]
        self.enhancement_level = buf[6] & 0x1F
        self.seal_count = buf[6] >> 5
        self.is_equipment = self.type in [0x01, 0x05, 0x06]
        self.num_grade = struct.unpack('I', buf[7:11])[0]
        self.endurance = struct.unpack('H', buf[11:13])[0]
        self.card_id = struct.unpack('I', buf[13:17])[0]
        # 增幅类型
        self.reinforce_type = buf[17]
        self.display_reinforce_type = reinforce_type_dict.get(self.reinforce_type)
        # 增幅等级
        self.reinforce_value = struct.unpack('H', buf[18:20])[0]
        self._others20_30 = buf[20:31]
        self.otherworld = buf[31:33]  # struct.unpack('H',item_bytes[31:33])[0]
        self._others32_36 = buf[33:37]
        self.magic_seal = buf[37:50]
        self.cover_magic_idx = buf[50]  # 表示被替换的魔法封印，当第四属性存在的时候有效

        self.forge_level = buf[51]
        self._others = buf[52:]

    def to_bytes(self) -> bytes:
        buf = b''
        buf += struct.pack('B', self.is_sealed)
        buf += struct.pack('B', self.type)
        buf += struct.pack('I', self.id)
        enhance_and_seal = self.enhancement_level | (self.seal_count << 5)
        buf += struct.pack('B', enhance_and_seal)
        buf += struct.pack('I', self.num_grade)
        buf += struct.pack('H', self.endurance)
        buf += struct.pack('I', self.card_id)
        buf += struct.pack('B', self.reinforce_type)
        buf += struct.pack('H', self.reinforce_value)
        buf += self._others20_30
        buf += self.otherworld  # struct.pack('H',self.otherworld)
        buf += self._others32_36
        magic_seal = (
            self.display_magic_seals[0].to_bytes()
            + self.display_magic_seals[1].to_bytes()
            + self.display_magic_seals[2].to_bytes()
            + self.magic_seal[9:10]
            + self.display_magic_seals[3].to_bytes()
            + struct.pack('B', self.cover_magic_idx)
        )
        buf += magic_seal
        buf += struct.pack('B', self.forge_level)
        buf += self._others
        return buf

    @staticmethod
    def default() -> 'DnfItemSlot':
        return DnfItemSlot(b'')

    @staticmethod
    def with_idx(idx: int) -> 'DnfItemSlot':
        item = DnfItemSlot(b'')
        item.display_idx = idx
        return item

    def __repr__(self):
        display_name = self.display_name
        if self.is_missing:
            display_name = '物品不存在'

        s = f'[{self.display_type}]{display_name}'
        if self.type in [0x02, 0x03, 0x04, 0x07, 0x0A]:
            s += f' 数量:{self.num_grade}'
        elif self.type == 0x01:
            if self.is_sealed != 0:
                s += '[封装]'
            if self.enhancement_level > 0:
                s += f' 强化+{self.enhancement_level}'
            s += f' 耐久:{self.endurance}'
            if self.reinforce_type != 0:
                s += f' 增幅:{self.display_reinforce_type}+{self.reinforce_value}'
            if self.forge_level > 0:
                s += f' 锻造:+{self.forge_level}'
            for it in self.display_magic_seals:
                if it.id == 0:
                    continue
                s += f' {it}'
            s += f' {self.display_rarity_name}'
        return s

    __str__ = __repr__
