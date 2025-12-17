from pathlib import Path

from config import config
from dnfpkgtool.repo.equipment_repo import EquipmentRepo

base_dir = Path(__file__).parent


def test_query():
    fp = config.get_equipment_parquet_file_path()
    equipment_repo = EquipmentRepo(str(fp))
    res = equipment_repo.query('', ['[coat]', '[shoes]'], 1, 20, 1)
    print()
    print(f'{len(res)} equipments found')
    for it in res:
        print(it)
