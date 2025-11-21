from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.quest_repo import build_quest_repo_parquet
from tests.repo.equipment_repo_test import base_dir


def test_build_quest_repo_parquet():
    pvf_path = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    reader = PVFReader(pvf_path)
    quest_list = reader.get_quest_list()
    build_quest_repo_parquet(quest_list, base_dir / 'data' / 'quests.parquet')
