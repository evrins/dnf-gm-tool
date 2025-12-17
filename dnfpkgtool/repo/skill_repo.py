from typing import List

import polars as pl
from loguru import logger

from dnfpkgtool.repo.base_repo import BaseRepo


class SkillRepo(BaseRepo):
    def query(
            self,
            name: str,
            job: str | None = None,
    ) -> List[dict]:
        name = name.lower()
        cond = pl.col('name').str.contains(name) | pl.col(
            'name2'
        ).str.to_lowercase().str.contains(name)

        if job is not None:
            cond = cond & (pl.col('job') == job)

        return self.df.filter(cond).select('*').to_dicts()

    def query_by_id(self, id_: int) -> dict | None:
        rs = self.df.filter(pl.col('id') == id_).limit(1).to_dicts()
        if len(rs) == 0:
            return None
        else:
            return rs[0]

    def query_by_job_and_id_of_job(self, job: str, id_of_job: int) -> dict | None:
        cond = pl.col('id_of_job') == id_of_job
        if job != 'all':
            cond = cond & (pl.col('job') == job)
        rs = self.df.filter(cond).select('*').limit(1).to_dicts()
        if len(rs) == 0:
            logger.warning(f'skill not found for job {job} and id of job {id_of_job}')
            return None
        else:
            return rs[0]
