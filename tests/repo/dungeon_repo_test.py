from pathlib import Path

from dnfpkgtool.repo.dungeon_repo import DungeonRepo

base_dir = Path(__file__).parent


def test_dungeon_build_unlock():
    repo = DungeonRepo(base_dir / 'data' / 'dungeons.parquet')
    res = repo.dungeon_unlock()
    print(res)
