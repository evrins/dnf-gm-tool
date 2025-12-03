import traceback
from pathlib import Path

from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.equipment_repo import EquipmentRepo, build_equipment_repo_parquet

base_dir = Path(__file__).parent


def test_build_equipment_repo():
    pvf_path = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    reader = PVFReader(pvf_path)
    equipment_list = reader.get_equipment_list()
    try:
        build_equipment_repo_parquet(
            equipment_list, base_dir / 'data' / 'equipments.parquet'
        )
    except Exception:
        traceback.print_exc()


def test_query():
    fp = config.get_equipment_parquet_file_path()
    equipment_repo = EquipmentRepo(str(fp))
    res = equipment_repo.query('', ['[coat]', '[shoes]'], 1, 20, 1)
    print()
    print(f'{len(res)} equipments found')
    for it in res:
        print(it)
