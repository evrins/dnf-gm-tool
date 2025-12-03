from pathlib import Path
from typing import Any, Dict, List

import polars as pl

from dnfpkgtool.repo import MappingElementLocation, remapping_pvf_list
from dnfpkgtool.repo.base_repo import BaseRepo
from loguru import logger


def build_skill_repo_parquet(pvf_list: List[Dict[str, Any]], fp: str | Path):
    mappings = [
        ('job', 'job', 0, MappingElementLocation.First),
        ('name', '[name]', '', MappingElementLocation.First),
        ('name2', '[name2]', '', MappingElementLocation.First),
        ('basic_explain', '[basic explain]', '', MappingElementLocation.First),
        ('explain', '[explain]', '', MappingElementLocation.First),
        (
            'feature_skill_index',
            '[feature skill index]',
            0,
            MappingElementLocation.First,
        ),
        ('skill_class', '[skill class]', 0, MappingElementLocation.First),
        ('id_of_job', 'id_of_job', 0, MappingElementLocation.First),
    ]
    df = remapping_pvf_list(pvf_list, mappings)
    df = pl.DataFrame(df)

    df.write_parquet(fp)


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
