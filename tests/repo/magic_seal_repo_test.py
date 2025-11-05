from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.magic_seal_repo import build_magic_seal_parquet


def test_build_magic_seal_parquet():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    magic_seal_dict = reader.get_magic_seal_dict()
    build_magic_seal_parquet(magic_seal_dict, config.get_magic_seal_parquet_file_path())
