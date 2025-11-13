import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool

from config.config import DbConfig


class DBManager:
    def __init__(self, config: DbConfig):
        self.config = config
        self.engines = {}

    def get_engine(self, db_name: str):
        if db_name not in self.engines:
            url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                self.config.username,
                self.config.password,
                self.config.host,
                self.config.port,
                db_name,
            )
            self.engines[db_name] = sqlalchemy.create_engine(
                url,
                poolclass=QueuePool,
                pool_size=5,  # Number of connections to keep open
                max_overflow=10,  # Additional connections when pool is exhausted
                pool_timeout=30,  # Seconds to wait before giving up on getting a connection
                pool_recycle=3600,  # Recycle connections after 1 hour
                pool_pre_ping=True,  # Verify connections before using them
            )
        return self.engines[db_name]

    def get_session(self, db_name: str):
        engine = self.get_engine(db_name)
        return Session(bind=engine)
