from dnfpkgtool.pvf.pvf_reader import PVFReader


def test_read_list_lite2():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    lst_file = reader.load_lst_file('character/character.lst')

    print(lst_file)


def test_range_10():
    for i in range(2, 13, 10):
        print(i)
