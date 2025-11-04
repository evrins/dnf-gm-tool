from pydantic import BaseModel


class MagicSeal(BaseModel):
    id: int = 0
    name: str = ''
    level: int = 0

    @staticmethod
    def from_bytes(buf: bytes) -> 'MagicSeal':
        id_ = buf[0]
        level = int.from_bytes(buf[1:], byteorder='big')

        return MagicSeal(id=id_, name='', level=level)

    def to_bytes(self) -> bytes:
        if self.id == 0:
            return b'\x00\x00\x00'
        buf = b''
        buf += self.id.to_bytes(1, 'big')
        buf += self.level.to_bytes(2, 'big')

        return buf

    def __repr__(self):
        return f'[{self.name}:{self.level}]'

    __str__ = __repr__
