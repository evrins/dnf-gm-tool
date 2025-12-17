import polars as pl

from dnfpkgtool.repo.base_repo import BaseRepo


class ExpRepo(BaseRepo):
    def query_by_level(self, level: int) -> int:
        cond = pl.col('level') == level

        return self.df.filter(cond).select('exp').limit(1).to_dicts()[0]['exp']
