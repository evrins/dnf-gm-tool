from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.quest_repo import build_quest_repo_parquet


def test_build_quest_repo_parquet():
    pvf_path = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    reader = PVFReader(pvf_path)
    quest_dict = reader.get_quest_dict()
    build_quest_repo_parquet(quest_dict, config.get_quest_parquet_file_path())
