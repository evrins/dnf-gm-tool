from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.exp_repo import build_exp_repo_parquet
from tests.repo.equipment_repo_test import base_dir


def test_build_exp_repo():
    config.load()
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    exp = reader.get_exp_table()
    build_exp_repo_parquet(exp, base_dir / 'data' / 'exps.parquet')
