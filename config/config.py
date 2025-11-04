import os
from pathlib import Path
from typing import List

import pymysql
from loguru import logger
from pydantic import BaseModel

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
    pvf_hash_list: List[str] = []


base_dir = Path(__file__).parent.parent

config_path = base_dir / 'data' / 'config.json'


def init_dirs():
    os.makedirs(base_dir / 'data', exist_ok=True)


class Config(BaseModel):
    db_config: DbConfig
    history: History
    pvf_hash: str = ''
    pvf_dir: Path = ''
    account_id: int = 0
    character_no: int = 0
    character_name: str = ''

    @staticmethod
    def default() -> 'Config':
        return Config(
            db_config=DbConfig(
                host='127.0.0.1',
                port=3306,
                username='root',
                password='123456',
            ),
            history=History(
                host_list=['localhost'],
                port_list=[3306],
                username_list=['root', 'game'],
                password_list=['123456', 'uu5!^%jg'],
            ),
        )

    def have_valid_pvf(self) -> bool:
        if not self.pvf_hash:
            return False

        for func in path_map.values():
            if not func(self.pvf_hash):
                return False

        return True


def load() -> Config:
    if not os.path.exists(config_path):
        return Config.default()
    with open(config_path, 'r') as f:
        json_data = f.read()
        cfg = Config.model_validate_json(json_data)
        cfg.pvf_dir = base_dir / 'data' / cfg.pvf_hash
        return cfg


_config: Config = load()


def save():
    with open(config_path, 'w') as f:
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

    return False


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


# todo build path from config


def build_stackable_parquet_file_path(pvf_hash: str) -> Path:
    return base_dir / 'data' / pvf_hash / 'stackable_parquet.parquet'


def get_stackable_parquet_file_path() -> Path:
    return build_stackable_parquet_file_path(_config.pvf_hash)


def build_equipment_parquet_file_path(pvf_hash: str) -> Path:
    return base_dir / 'data' / pvf_hash / 'equipments.parquet'


def get_equipment_parquet_file_path() -> Path:
    return build_equipment_parquet_file_path(_config.pvf_hash)


def build_magic_seal_parquet_file_path(pvf_hash: str) -> Path:
    return base_dir / 'data' / pvf_hash / 'magic_seals.parquet'


def get_magic_seal_parquet_file_path() -> Path:
    return build_magic_seal_parquet_file_path(_config.pvf_hash)


def build_skill_parquet_parquet_file_path(pvf_hash: str) -> Path:
    return base_dir / 'data' / pvf_hash / 'skills.parquet'


def get_skill_parquet_file_path() -> Path:
    return build_skill_parquet_parquet_file_path(_config.pvf_hash)


def build_orb_parquet_file_path(pvf_hash: str) -> Path:
    return base_dir / 'data' / pvf_hash / 'orbs.parquet'


def get_orb_parquet_file_path() -> Path:
    return build_orb_parquet_file_path(_config.pvf_hash)


path_map = {
    'stackable': build_stackable_parquet_file_path,
    'equipment': build_equipment_parquet_file_path,
    'magic_seal': build_magic_seal_parquet_file_path,
    'skill': build_skill_parquet_parquet_file_path,
    'orb': build_orb_parquet_file_path,
}


def create_pvf_dir(pvf_hash: str) -> bool:
    pvf_dir = base_dir / 'data' / pvf_hash
    if pvf_dir.exists():
        return True
    pvf_dir.mkdir()
    return False


def set_pvf_hash(pvf_hash: str):
    _config.pvf_hash = pvf_hash
    _config.pvf_dir = base_dir / 'data' / pvf_hash

    history = _config.history
    if pvf_hash not in history.pvf_hash_list:
        history.pvf_hash_list.append(pvf_hash)
    _config.history = history

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
