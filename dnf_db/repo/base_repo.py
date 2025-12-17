import threading

from config.config import get_db_config
from dnf_db.db_manager import DBManager
from dnf_db.entity.signals import gs

# Singleton DBManager instance to reuse connection pools
_db_manager: DBManager | None = None
_db_manager_lock = threading.Lock()


def clean_db_manager():
    global _db_manager
    with _db_manager_lock:
        _db_manager = None


gs.db_config_changed.connect(clean_db_manager)


def get_db_manager() -> DBManager:
    global _db_manager
    if _db_manager is None:
        with _db_manager_lock:
            # Double-check pattern: recheck after acquiring lock
            if _db_manager is None:
                db_config = get_db_config()
                _db_manager = DBManager(db_config)
    return _db_manager


class BaseRepo:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_engine(self):
        return get_db_manager().get_engine(self.db_name)
