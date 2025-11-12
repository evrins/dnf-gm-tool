"""
Dungeon Repository Module

This module provides functionality for managing dungeon data from PVF files.
It includes methods for building parquet files from dungeon data and
generating unlock strings for dungeons.
"""

from pathlib import Path

import polars as pl

from dnfpkgtool.pvf.pvf_reader import PVFDict
from dnfpkgtool.repo import MappingElementLocation, remapping_pvf_dict
from dnfpkgtool.repo.base_repo import BaseRepo


def build_dungeon_repo_parquet(pvf_dict: PVFDict, fp: str | Path):
    mappings = [
        ('explain', '[explain]', '', MappingElementLocation.First),
        ('basis_level', '[basis level]', 0, MappingElementLocation.First),
        (
            'minimum_required_level',
            '[minimum required level]',
            0,
            MappingElementLocation.First,
        ),
    ]

    df = remapping_pvf_dict(pvf_dict, mappings)
    df = pl.DataFrame(df)
    df = df.drop('name2')

    df.write_parquet(fp)


class DungeonRepo(BaseRepo):
    def dungeon_unlock(self) -> str:
        """
        Generate a comma-separated string of dungeon IDs with unlock level (|3)
        Returns: String like "1|3,2|3,3|3,..."
        """

        res = []
        for it in self.df.select('id').sort('id').to_series().to_list():
            res.append(f'{it}|3')

        return ','.join(res)


