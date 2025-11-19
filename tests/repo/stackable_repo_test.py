from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.stackable_repo import StackableRepo, build_stackable_repo_parquet
from tests.repo.equipment_repo_test import base_dir


def test_build_stackable_repo_parquet():
    pvf_path = '/Users/evrins/workspace/python/dnf_gm_tool/Script.璀璨.pvf'
    reader = PVFReader(pvf_path)
    stackable_dict = reader.get_stackable_dict()
    build_stackable_repo_parquet(
        stackable_dict, base_dir / 'data' / 'stackables.parquet'
    )


def test_query():
    fp = config.get_stackable_parquet_file_path()
    stackable_repo = StackableRepo(str(fp))
    rs = stackable_repo.query('药', max_level=50)
    print(len(rs))


def test_query_by_id():
    fp = config.get_stackable_parquet_file_path()
    stackable_repo = StackableRepo(str(fp))
    res = stackable_repo.query_by_id(1)
    print()
    print(res)
