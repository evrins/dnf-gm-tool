from config.config import get_db_config
from dnfpkgtool.db.db_manager import DBManager


class BaseRepo:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_engine(self):
        db_config = get_db_config()
        dbm = DBManager(db_config)
        return dbm.get_engine(self.db_name)
