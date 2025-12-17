from typing import List

import polars as pl

from dnfpkgtool.repo.base_repo import BaseRepo


class MagicSealRepo(BaseRepo):
    def query_by_id(self, id_: int) -> dict:
        rs = self.df.filter(pl.col('id') == id_).select('*').limit(1).to_dicts()
        return rs[0]

    def query_all(self) -> List[dict]:
        rs = self.df.select('*').to_dicts()
        return rs
