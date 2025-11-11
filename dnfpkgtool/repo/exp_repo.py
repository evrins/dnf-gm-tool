from pathlib import Path
from typing import List

import polars as pl
from loguru import logger

from config import config
from dnfpkgtool.repo.base_repo import BaseRepo


def build_exp_repo_parquet(exp_list: List[int], fp: str | Path):
    exp_list = [0] + exp_list
    n = len(exp_list)
    df = {
        'level': range(1, n + 1),
        'exp': exp_list,
    }
    df = pl.DataFrame(df)

    df.write_parquet(fp)


class ExpRepo(BaseRepo):
    df: pl.DataFrame | None

    def __init__(self, fp: str | Path):
        self._is_available = True
        try:
            self.df = pl.read_parquet(fp)
        except Exception as e:
            logger.warning(f'ExpRepo failed to load parquet file {fp}: {e}')
            # Create an empty dataframe with the expected schema
            self.df = None
            self._is_available = False

    def is_available(self) -> bool:
        """Check if the repository is available (parquet file loaded successfully)"""
        return self._is_available

    def query_by_level(self, level: int) -> int:
        cond = pl.col('level') == level

        return self.df.filter(cond).select('exp').limit(1).to_dicts()[0]['exp']


def get_exp_repo():
    fp = config.get_exp_repo_parquet_file_path()
    return ExpRepo(fp)
