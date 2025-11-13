from pathlib import Path
from typing import List

import polars as pl

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
    def query_by_level(self, level: int) -> int:
        cond = pl.col('level') == level

        return self.df.filter(cond).select('exp').limit(1).to_dicts()[0]['exp']
