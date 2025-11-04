from dnfpkgtool.db.repo.account_cargo_repo import AccountCargoRepo
from dnfpkgtool.db.service.item_service import ItemService, build_repo_parquet


def test_unpack_blob_items():
    repo = AccountCargoRepo()
    account_cargo = repo.query_by_m_id(18000000)
    svc = ItemService()
    items = svc.unpack_blob_items(account_cargo.cargo)
    for it in items:
        print(f'{it}')


def test_unpack_blob_item():
    buf = bytes.fromhex(
        '010180a7220001236a00001b000000000000000000000000000000000000000000000000008e000a020014f4001e91c100280000000000000000000000'
    )
    svc = ItemService()
    item = svc.unpack_blob_item(buf)
    print(item)


def test_unpack_blob_item_1():
    buf = bytes.fromhex(
        '010183242300001869fc2d28000000000000000000c30b0000c6d9e068c402000000000000580b184c12175a10157a0000000000000000000000000000'
    )
    svc = ItemService()
    item = svc.unpack_blob_item(buf)
    for offset in range(1, 8):
        for it in item.display_magic_seals:
            if it.id == 0:
                continue
            print(f'{it.id} {it.name} {it.level} {(it.level + offset) % 8}')
        print('-' * 8)
    print(item)


def test_unpack_blob_item_2():
    buf = b'\x00\x01i\xca\x06\x00\x0f\xeb~\xcd\x0b\x00\x00\xb9\xb4\x98\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    svc = ItemService()
    item = svc.unpack_blob_item(buf)
    print(item)


def test_unpack_blob_item_3():
    buf1 = b'\xdc\x02\x00\x00x\x9cc`\x94I0f\x13\xb8R\xe4"\xa6\xc8 \xc0\xc7\xc0\xc0\xcc\xc0\xc0p\x98\x9b\x81a\xdb\xc2\xdb\x19!\x8c\x0c\xf8\x01\xa3K\xef\x1dq\x06o\xceLC\x02\n\xb1j\x8e\xe5gb\xe07\xcb\xedt\xd1\x00\xf3\x816\xb3\xc1l\x0e"h\xb3\xec\x13f\x06\xfe\x06en\x11\x05\x98f\x16\xe2m\xde\xfb\x13h\xb3p\xd7\rCE\x98ff\x98\xcd\xc1\x04m\xbe\xbb\x83\x95\x81\xff\xa0\xe6)M)\x86\x93[g\x80\x03\x8cx\x9bk\xcf\xb10\xf0_\xb2\x17T\x92\x84\xd9\xccD\xbcfM=6\x06\xfe\x140{&4\xaa\x88\xd7l\x19\n\xd4\\\xf4}E29\x9a\x05\xe3\x18\x80\x01\xb6\xf9w\x129\x9a3O\x01m~]w\x96\x1b\xc2\'Ms\xe5G\xb8\x9fI\xd5\x0c\x00\xcc\x90.\xb9'
    svc = ItemService()
    item_list = svc.unpack_blob_items(buf1)
    print(item_list)

    buf2 = b'\xdc\x02\x00\x00x\x9cc`\x94I0f\x13\xb8R\xe4"\xa6\xc8 \xc0\xc7\xc0\xc0\xcc\xc0\xc0p\x98\x9b\x81a\xdb\xc2\xdb\x19!\x8c\x0c\xf8\x01\xa3K\xef\x1dq\x06o\xceLC\x02\n\xb1j\x8e\xe5gb\xe07\xcb\xedt\xd1\x00\xf3\x816\xb3\xc1l\x0e"h\xb3\xec\x13f\x06\xfe\x06en\x11\x05\x98f\x16\xe2m\xde\xfb\x13h\xb3p\xd7\rCE\x98ff\x98\xcd\xc1\x04m\xbe\xbb\x83\x95\x81\xff\xa0\xe6)M)\x86\x93[g\x80\x03\x8cx\x9bk\xcf\xb10\xf0_\xb2\x17T\x92\x84\xd9\xccD\xbcfM=6\x06\xfe\x140{&4\xaa\x88\xd7l\x19\n\xd4\\\xf4}E29\x9a\x05\xe3\x18\x80\x01\xb6\xf9w\x12\xa9\x9a\x193O\x01\xad}]w\x96\x1b\xc2\'\xcd\xda\xca\x8fp\x0f\x93\xaa\x19\x00P\xc1.\xb9'
    item_list2 = svc.unpack_blob_items(buf2)
    print(item_list2)


def test_unpack_blob_item_4():
    buf = b'\x00\x01\x1c`3\x06\x10\xd4rD\x16!\x00\x10\x0e\x00\x00\x03\x00\x00\x00\xc3\x0b\x00\x00\xb6\xa1\xdbhT\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    svc = ItemService()
    item = svc.unpack_blob_item(buf)
    buf2 = item.to_bytes()
    assert buf2 == buf


def test_get_current_character_cargo():
    svc = ItemService()
    items = svc.get_current_character_cargo()
    for it in items:
        print(f'{it}')


def test_get_current_character_inventory():
    svc = ItemService()
    ci = svc.get_current_character_inventory()
    print('equipments:')
    for it in ci.equipments:
        print(f'{it}')

    print('creatures:')
    for it in ci.creatures:
        print(f'{it}')

    print('backpack:')
    for it in ci.backpack:
        print(f'{it}')


def test_build_repo_parquet():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    build_repo_parquet(pvf_path)
