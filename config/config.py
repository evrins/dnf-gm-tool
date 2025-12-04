import os
import shutil
from pathlib import Path
from typing import List

import pymysql
from loguru import logger
from pydantic import BaseModel

from config.config_saver import get_config_saver_manager
from dnfpkgtool.db.entity.signals import gs


class DbConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str


class History(BaseModel):
    host_list: List[str]
    port_list: List[int]
    username_list: List[str]
    password_list: List[str]


base_dir = Path(__file__).parent.parent


def get_config_path() -> Path:
    return base_dir / 'data' / 'config.json'


def set_base_dir(dir_: Path):
    global base_dir
    base_dir = dir_


def get_base_dir() -> Path:
    return base_dir


def init_dirs():
    os.makedirs(base_dir / 'data' / 'log', exist_ok=True)


class Pvf(BaseModel):
    remark: str = ''
    uuid: str
    encoding: int


class Config(BaseModel):
    db_config: DbConfig
    pvf_list: List[Pvf] = []
    history: History
    pvf_uuid: str = ''
    pvf_dir: Path = ''
    account_id: int = 0
    character_no: int = 0
    character_name: str = ''

    @staticmethod
    def default() -> 'Config':
        return Config(
            db_config=DbConfig(
                host='192.168.200.131',
                port=3306,
                username='root',
                password='123456',
            ),
            pvf_list=[],
            history=History(
                host_list=['localhost', '192.168.200.131'],
                port_list=[3306],
                username_list=['root', 'game'],
                password_list=['123456', 'uu5!^%jg'],
            ),
        )

    def have_valid_pvf(self) -> bool:
        if not self.pvf_uuid:
            return False

        for func in path_map.values():
            if not func(self.pvf_uuid):
                return False

        return True


_config: Config = None


def load():
    global _config
    if not os.path.exists(get_config_path()):
        _config = Config.default()
    else:
        with open(get_config_path(), 'r', encoding='utf-8') as f:
            json_data = f.read()
            cfg = Config.model_validate_json(json_data)
            cfg.pvf_dir = base_dir / 'data' / cfg.pvf_uuid
            _config = cfg


def save():
    """Save config asynchronously using worker thread."""

    config_json = _config.model_dump_json(indent=4)
    config_path = get_config_path()

    # Use worker thread for async save
    saver = get_config_saver_manager()
    saver.save_config_async(config_path, config_json)


def save_sync():
    """Save config synchronously (blocking). Use only when necessary."""
    with open(get_config_path(), 'w') as f:
        f.write(_config.model_dump_json(indent=4))


def save_db_config(host: str, port: int, username: str, password: str):
    _config.db_config = DbConfig(
        host=host,
        port=port,
        username=username,
        password=password,
    )

    history = _config.history
    if host not in history.host_list:
        history.host_list.append(host)

    if port not in history.port_list:
        history.port_list.append(port)

    if username not in history.username_list:
        history.username_list.append(username)

    if password not in history.password_list:
        history.password_list.append(password)

    _config.history = history
    save()


def get_config() -> Config:
    return _config


def get_db_config() -> DbConfig:
    return _config.db_config


def get_log_dir() -> Path:
    return base_dir / 'data' / 'log'


def check_mysql_config(
        host: str,
        port: int,
        user: str,
        password: str,
) -> bool:
    conn = None
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database='d_taiwan',
            connect_timeout=2,
        )

        conn.ping(True)

    except pymysql.Error as err:
        logger.error(f'error connecting to database: {err}')
        return False
    finally:
        if conn and conn.open:
            conn.close()
            logger.info('database connection closed')
    return True


def get_db_conn(db_name: str) -> pymysql.Connection:
    db_config = get_db_config()
    conn = pymysql.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        passwd=db_config.password,
        database=db_name,
        connect_timeout=2,
    )

    conn.ping(True)

    return conn


def get_current_account_id():
    return _config.account_id


def get_current_character_no():
    return _config.character_no


def have_valid_account_id_and_character_no() -> bool:
    return _config.account_id > 0 and _config.character_no > 0


# todo build path from config


def build_stackable_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'stackables.parquet'


def get_stackable_parquet_file_path() -> Path:
    return build_stackable_parquet_file_path(_config.pvf_uuid)


def build_equipment_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'equipments.parquet'


def get_equipment_parquet_file_path() -> Path:
    return build_equipment_parquet_file_path(_config.pvf_uuid)


def build_magic_seal_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'magic_seals.parquet'


def get_magic_seal_parquet_file_path() -> Path:
    return build_magic_seal_parquet_file_path(_config.pvf_uuid)


def build_skill_parquet_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'skills.parquet'


def get_skill_parquet_file_path() -> Path:
    return build_skill_parquet_parquet_file_path(_config.pvf_uuid)


def build_orb_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'orbs.parquet'


def get_orb_parquet_file_path() -> Path:
    return build_orb_parquet_file_path(_config.pvf_uuid)


def build_quest_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'quests.parquet'


def get_quest_parquet_file_path() -> Path:
    return build_quest_parquet_file_path(_config.pvf_uuid)


def build_exp_repo_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'exps.parquet'


def get_exp_repo_parquet_file_path() -> Path:
    return build_exp_repo_parquet_file_path(_config.pvf_uuid)


def build_dungeon_repo_parquet_file_path(uuid: str) -> Path:
    return base_dir / 'data' / uuid / 'dungeons.parquet'


def build_pvf_dir(uuid: str) -> Path:
    return base_dir / 'data' / uuid


def get_dungeon_repo_parquet_file_path() -> Path:
    return build_dungeon_repo_parquet_file_path(_config.pvf_uuid)


path_map = {
    'stackable': build_stackable_parquet_file_path,
    'equipment': build_equipment_parquet_file_path,
    'magic_seal': build_magic_seal_parquet_file_path,
    'skill': build_skill_parquet_parquet_file_path,
    'orb': build_orb_parquet_file_path,
    'quest': build_quest_parquet_file_path,
    'exp': build_exp_repo_parquet_file_path,
    'dungeon': build_dungeon_repo_parquet_file_path,
}


def create_pvf_dir(uuid: str) -> bool:
    pvf_dir = base_dir / 'data' / uuid
    if pvf_dir.exists():
        return True
    pvf_dir.mkdir()
    return False


def set_pvf_uuid(uuid: str):
    _config.pvf_uuid = uuid
    _config.pvf_dir = base_dir / 'data' / uuid

    save()

    gs.pvf_changed.emit()


def set_account_id_and_character_no(
        account_id: int, character_no: int, character_name: str
):
    _config.account_id = account_id
    _config.character_no = character_no
    _config.character_name = character_name

    save()

    gs.account_id_changed.emit()
    gs.character_no_changed.emit()


MAX_GRADE = 232


def get_pvf_list() -> List[Pvf]:
    return _config.pvf_list


def add_pvf(it: Pvf):
    _config.pvf_list.append(it)
    save()


def update_pvf_by_uuid(uuid: str, remark: str):
    n = len(_config.pvf_list)
    for i in range(n):
        if _config.pvf_list[i].uuid == uuid:
            _config.pvf_list[i].remark = remark
            break
    save()


def delete_pvf_by_uuid(uuid: str):
    if not uuid:
        return
    _config.pvf_list = [it for it in _config.pvf_list if it.uuid != uuid]
    dir_name = build_pvf_dir(uuid)
    shutil.rmtree(dir_name)
    save()
