from util import calculate_hash_of_file


def test_calculate_hash_of_file() -> str:
    fp = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    res = calculate_hash_of_file(fp)
    print(f'{fp}: {res}')
