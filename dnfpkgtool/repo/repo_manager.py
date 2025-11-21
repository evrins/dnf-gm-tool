from typing import Callable, Dict

from config import config
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.repo.base_repo import BaseRepo
from dnfpkgtool.repo.dungeon_repo import DungeonRepo
from dnfpkgtool.repo.equipment_repo import EquipmentRepo
from dnfpkgtool.repo.exp_repo import ExpRepo
from dnfpkgtool.repo.magic_seal_repo import MagicSealRepo
from dnfpkgtool.repo.orb_repo import OrbRepo
from dnfpkgtool.repo.quest_repo import QuestRepo
from dnfpkgtool.repo.skill_repo import SkillRepo
from dnfpkgtool.repo.stackable_repo import StackableRepo

repo_path_getter = Callable[[], str]

repo_cache: Dict[str, BaseRepo] = {}

repo_config = {
    'equipment': (EquipmentRepo, config.get_equipment_parquet_file_path),
    'stackable': (StackableRepo, config.get_stackable_parquet_file_path),
    'exp': (ExpRepo, config.get_exp_repo_parquet_file_path),
    'magic_seal': (MagicSealRepo, config.get_magic_seal_parquet_file_path),
    'orb': (OrbRepo, config.get_orb_parquet_file_path),
    'quest': (QuestRepo, config.get_quest_parquet_file_path),
    'skill': (SkillRepo, config.get_skill_parquet_file_path),
    'dungeon': (DungeonRepo, config.get_dungeon_repo_parquet_file_path),
}


def refresh():
    for k, v in repo_cache.items():
        _, path_getter = repo_config[k]
        v.init_df(path_getter())


gs.pvf_changed.connect(refresh)


def get_repo(repo_name: str):
    repo = repo_cache.get(repo_name, None)
    if repo is None:
        repo_class, path_getter = repo_config.get(repo_name)
        repo = repo_class(path_getter())
        repo_cache[repo_name] = repo
    return repo


def get_equipment_repo() -> EquipmentRepo:
    return get_repo('equipment')


def get_stackable_repo() -> StackableRepo:
    return get_repo('stackable')


def get_exp_repo() -> ExpRepo:
    return get_repo('exp')


def get_magic_seal_repo() -> MagicSealRepo:
    return get_repo('magic_seal')


def get_orb_repo() -> OrbRepo:
    return get_repo('orb')


def get_quest_repo() -> QuestRepo:
    return get_repo('quest')


def get_skill_repo() -> SkillRepo:
    return get_repo('skill')


def get_dungeon_repo() -> DungeonRepo:
    return get_repo('dungeon')
