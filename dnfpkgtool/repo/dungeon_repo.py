"""
Dungeon Repository Module

This module provides functionality for managing dungeon data from PVF files.
It includes methods for building parquet files from dungeon data and
generating unlock strings for dungeons.
"""

from dnfpkgtool.repo.base_repo import BaseRepo


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
