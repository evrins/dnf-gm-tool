from pathlib import Path

import polars as pl
from loguru import logger


class BaseRepo:
    _is_available = False
    df: pl.DataFrame | None

    def __init__(self, fp: str | Path):
        self.init_df(fp)

    def is_available(self) -> bool:
        return self._is_available

    def init_df(self, fp: str | Path):
        try:
            self.df = pl.read_parquet(fp)
            self._is_available = True
        except Exception as e:
            logger.warning(
                f'{self.__class__.__name__} failed to load parquet file {fp}: {e}'
            )
            # Create an empty dataframe with the expected schema
            self.df = None
            self._is_available = False
