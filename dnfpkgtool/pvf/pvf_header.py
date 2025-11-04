import struct

from pydantic import BaseModel

from util import decrypt_bytes


class LeafNode(BaseModel):
    index: int = 0
    fn: int = 0
    file_path: str = ''
    file_length: int = 0
    file_crc32: int = 0
    relative_offset: int = 0


class PVFHeader(BaseModel):
    uuid: bytes = b''
    version: bytes = b''
    leaf_dict: dict[str, LeafNode] = {}
    header_len: int = 0
    dir_tree_len: int = 0
    file_pack_index_shift: int = 0


def parse_pvf_header(f) -> PVFHeader:
    header = PVFHeader()

    uuid_len = struct.unpack('i', f.read(4))[0]
    header.uuid = f.read(uuid_len)
    header.version = struct.unpack('i', f.read(4))[0]
    dir_tree_len = struct.unpack('i', f.read(4))[0]
    dir_tree_crc32 = struct.unpack('I', f.read(4))[0]
    num_files_in_dir_tree = struct.unpack('I', f.read(4))[0]

    header.header_len = f.tell()
    header.dir_tree_len = dir_tree_len
    header.file_pack_index_shift = f.tell() + dir_tree_len

    header_tree_bytes = f.read(dir_tree_len)
    header_tree_decrypted = decrypt_bytes(header_tree_bytes, dir_tree_crc32)

    # parse leafs
    leaf_dict: dict[str, LeafNode] = parse_leafs(
        header_tree_decrypted, num_files_in_dir_tree
    )
    header.leaf_dict = leaf_dict

    return header


def parse_leafs(
    header_bytes: bytes, num_of_files_in_dir_tree: int
) -> dict[str, LeafNode]:
    current_index = 0
    leafs = {}
    for _ in range(num_of_files_in_dir_tree):
        leaf, current_index = parse_leaf(header_bytes, current_index)
        leafs[leaf.file_path] = leaf

    return leafs


def parse_leaf(header_bytes: bytes, index: int) -> tuple[LeafNode, int]:
    leaf_node = LeafNode()
    leaf_node.index = index

    fn_bytes = header_bytes[index : index + 4]
    index += 4
    file_path_length_bytes = header_bytes[index : index + 4]
    index += 4
    file_path_length = struct.unpack('I', file_path_length_bytes)[0]
    file_path_bytes = header_bytes[index : index + file_path_length]
    index += file_path_length
    file_length_bytes = header_bytes[index : index + 4]
    index += 4
    file_crc32_bytes = header_bytes[index : index + 4]
    index += 4
    relative_offset_bytes = header_bytes[index : index + 4]
    index += 4

    leaf_node.fn = struct.unpack('I', fn_bytes)[0]
    leaf_node.file_path = file_path_bytes.decode(errors='replace')
    leaf_node.file_length = (struct.unpack('I', file_length_bytes)[0] + 3) & 0xFFFFFFFC
    leaf_node.file_crc32 = struct.unpack('I', file_crc32_bytes)[0]
    leaf_node.relative_offset = struct.unpack('I', relative_offset_bytes)[0]

    return leaf_node, index


class PVFHeader_:
    def __init__(self, path, readFullFile=False):
        fp = open(path, 'rb')
        self.pvfPath = path
        self.uuid_len = struct.unpack('i', fp.read(4))[0]
        self.uuid = fp.read(self.uuid_len)
        self.PVFversion = struct.unpack('i', fp.read(4))[0]
        self.dirTreeLength = struct.unpack('i', fp.read(4))[0]  # 长度
        self.dirTreeCrc32 = struct.unpack('I', fp.read(4))[0]
        self.numFilesInDirTree: int = struct.unpack('I', fp.read(4))[0]
        self.filePackIndexShift = fp.tell() + self.dirTreeLength
        self.headerLength = fp.tell()
        # 读内部文件树头
        headerTreeBytes = fp.read(self.dirTreeLength)
        # int_num = header.dirTreeLength//4
        self.headerTreeBytes = headerTreeBytes
        self.unpackedHeaderTreeDecrypted = decrypt_bytes(
            headerTreeBytes, self.dirTreeCrc32
        )
        self.index = 0  # 用于读取HeaderTree的指针
        self.fp = fp
        # tmp_index = fp.tell()
        if readFullFile:
            self.filePackBytes = fp.read()
            fp.seek(0)
            self.fullFile = fp.read()
        else:
            self.ullFile = None
        # fp.close()

    def to_bytes(self, CRC: int, fileNum=0, treeLength=0, uuid=b'\x00' * 36):
        if fileNum == 0:
            fileNum = self.numFilesInDirTree
        if treeLength == 0:
            treeLength = self.dirTreeLength
        # CRC = zlib.crc32(treechunk,fileNum).to_bytes(4,'little')
        res = bytearray()
        res += len(uuid).to_bytes(4, 'little')
        res += uuid
        res += self.PVFversion.to_bytes(4, 'little')
        res += treeLength.to_bytes(4, 'little')
        res += CRC.to_bytes(4, 'little')  # dirTreeCrc32.to_bytes(4,'little')
        res += fileNum.to_bytes(4, 'little')
        # print(res)
        print('pvfHeader:', len(res), res)
        return res

    def get_Header_Tree_Bytes(self, byte_num=4):
        res = self.unpackedHeaderTreeDecrypted[self.index : self.index + byte_num]
        self.index += byte_num
        return res

    def read_bytes(self, startIndex, length):
        if self.fullFile is not None:
            return self.fullFile[startIndex : startIndex + length]
        else:
            if self.fp is None:
                self.fp = open(self.pvfPath, 'rb')
            self.fp.seek(startIndex)
            return self.fp.read(length)

    def __repr__(self):
        return f'PVF [{self.uuid.decode()}]\nVer:{self.PVFversion}\nTreeLength:{self.dirTreeLength} \nCRC:{hex(self.dirTreeCrc32)}\n{self.numFilesInDirTree} files'

    __str__ = __repr__
