from pathlib import Path
from typing import List

import polars as pl

from dnfpkgtool.pvf.pvf_reader import PVFDict
from dnfpkgtool.repo import (
    MappingElementLocation,
    remapping_pvf_dict,
)
from dnfpkgtool.repo.base_repo import BaseRepo

quest_type_list = [
    '[assault count]',
    '[get item]',
    '[condition under clear]',
    '[ui click]',
    '[seeking]',
    '[send chatting]',
    '[get score]',
    '[meet npc]',
    '[custom quest]',
    '[seek n meet npc]',
    '[equipped item]',
    '[check time]',
    '[disjoint item]',
    '[hunt enemy]',
    '[clear quest]',
    '[amplify item]',
    '[use item]',
    '[clear map]',
    '[use fortune coin]',
    '[hunt monster]',
]


def build_quest_repo_parquet(pvf_dict: PVFDict, fp: str | Path):
    mappings = [
        ('grade', '[grade]', '', MappingElementLocation.First),
        ('difficulty', '[difficulty]', '', MappingElementLocation.First),
        ('quest_type', '[type]', '', MappingElementLocation.First),
        ('int_data', '[int data]', [], MappingElementLocation.All),
    ]
    df = remapping_pvf_dict(pvf_dict, mappings)
    del df['name2']
    df = pl.DataFrame(df)

    df.write_parquet(fp)


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

    def query_by_id(self, id_: int) -> dict:
        return self.df.filter(pl.col('id') == id_).limit(1).to_dicts()[0]

    def query_by_job_and_id_of_job(self, job: str, id_of_job: int) -> dict:
        cond = pl.col('id_of_job') == id_of_job
        if job != 'all':
            cond = cond & (pl.col('job') == job)
        return self.df.filter(cond).select('*').limit(1).to_dicts()[0]


