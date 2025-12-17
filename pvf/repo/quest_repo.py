from typing import List

import polars as pl

from pvf.repo.base_repo import BaseRepo


class QuestRepo(BaseRepo):
    def query(
        self,
        name: str,
        job: str | None = None,
    ) -> List[dict]:
        name = name.lower()
        cond = pl.col('name').str.contains(name)

        if job is not None:
            cond = cond & (pl.col('job') == job)

        return self.df.filter(cond).select('*').to_dicts()

    def query_by_id(self, id_: int) -> dict | None:
        res = self.df.filter(pl.col('id') == id_).limit(1).to_dicts()
        if not res:
            return None
        return res[0]

    def query_by_job_and_id_of_job(self, job: str, id_of_job: int) -> dict:
        cond = pl.col('id_of_job') == id_of_job
        if job != 'all':
            cond = cond & (pl.col('job') == job)
        return self.df.filter(cond).select('*').limit(1).to_dicts()[0]
