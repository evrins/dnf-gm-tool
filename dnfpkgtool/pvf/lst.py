import struct

from dnfpkgtool.pvf.string_table import StringTable


class Lst(object):
    def __init__(
            self,
            content_bytes: bytes,
            string_table: StringTable,
            encode='big5',
            base_dir='',
    ):
        self.ver_code = content_bytes[:2]
        self.table_dict: dict[int, str] = {}
        self.string_table = string_table
        self.encode = encode
        self.base_dir = base_dir

        for i in range(2, len(content_bytes) - 9, 10):
            a, aa, b, bb = struct.unpack('<bIbI', content_bytes[i : i + 10])
            if a == 2:
                index = aa
            elif a == 7:
                string_index = aa

            if b == 2:
                index = bb
            elif b == 7:
                string_index = bb

            string = self.string_table[string_index]
            self.table_dict[index] = string

    def __getitem__(self, item):
        return self.table_dict[item]

    def __len__(self):
        return len(self.table_dict)

    def __repr__(self):
        count = 0
        buf = []
        for k, v in self.table_dict.items():
            if count > 10:
                continue
            buf.append(f'{k}: {v}')

        return 'Lst object. <' + ','.join(buf) + '...>'

    __str__ = __repr__
