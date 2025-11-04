import math
import struct

from cachetools import LRUCache, cached
from zhconv import convert


class StringTable:
    """stringtable.bin文件对象"""

    def __init__(self, buf: bytes, encode='big5') -> None:
        self.encode = encode
        self.length = struct.unpack('I', buf[:4])[0]  # 字符串数量
        self.buf = buf[4:]  # 4+self.length*4*2
        self.convertChunk = []

    def __getitem__(self, n: int) -> str:
        # 指第n和n+1个int，不是第n组int
        return convert(self._get_item(n), 'zh-cn')

    @cached(cache=LRUCache(maxsize=math.inf))
    def _get_item(self, n: int) -> str:
        index = struct.unpack('<II', self.buf[n * 4 : n * 4 + 8])
        value = self.buf[index[0] : index[1]].decode(self.encode, 'ignore')
        return value

    # todo remove it some day
    def convertZhcn(self):
        self.convertChunk = [''] * self.length * 2
        for i in range(self.length * 2):
            value = self._get_item(i)
            self.convertChunk[i] = convert(value, 'zh-cn')
        self.converted = True
