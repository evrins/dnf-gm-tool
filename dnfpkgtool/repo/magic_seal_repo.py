from pathlib import Path
from typing import List

import polars as pl
from loguru import logger

from config import config
from dnfpkgtool.repo.base_repo import BaseRepo


def build_magic_seal_parquet(magic_seal_dict: dict[int, str], out_path: str | Path):
    df = {'id': [], 'name': []}
    for k, v in magic_seal_dict.items():
        df['id'].append(k)
        df['name'].append(v)
    df = pl.DataFrame(df)

    df.write_parquet(out_path)


class MagicSealRepo(BaseRepo):
    def __init__(self, fp: str | Path):
        self._is_available = True
        try:
            self.df = pl.read_parquet(fp)
        except Exception as e:
            logger.warning(f'MagicSealRepo failed to load parquet file {fp}: {e}')
            # Create an empty dataframe with the expected schema
            self.df = None
            self._is_available = False

    def is_available(self) -> bool:
        """Check if the repository is available (parquet file loaded successfully)"""
        return self._is_available

    def query_by_id(self, id_: int) -> dict:
        rs = self.df.filter(pl.col('id') == id_).select('*').limit(1).to_dicts()
        return rs[0]

    def query_all(self) -> List[dict]:
        rs = self.df.select('*').to_dicts()
        return rs


def get_magic_seal_repo() -> MagicSealRepo:
    fp = config.get_magic_seal_parquet_file_path()
    return MagicSealRepo(fp)
