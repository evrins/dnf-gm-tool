from typing import List

import polars as pl
from loguru import logger

from dnfpkgtool.repo.base_repo import BaseRepo
from util import time_it


class EquipmentIdNotFoundException(Exception):
    def __init__(self, ep_id):
        self.ep_id = ep_id

        super().__init__('Equipment ID not found')

    def __str__(self):
        return f'Equipment ID not found: {self.ep_id}'


class EquipmentRepo(BaseRepo):
    @time_it
    def query(
            self,
            name: str,
            equipment_type_list: List[str] | None = None,
            usable_job: str | None = None,
            item_group_name: str | None = None,
            armor_type: str | None = None,
            min_level: int | None = None,
            max_level: int | None = None,
            rarity: str | None = None,
            limit: int | None = None,
    ):
        logger.info(
            f'querying {name} equipment types {equipment_type_list} usable job {usable_job} item group {item_group_name} armor_type {armor_type} min_level {min_level} max_level {max_level} rarity {rarity}'
        )

        name = name.lower()
        cond = (pl.col('name').str.contains(name)) | (
            pl.col('name2').str.to_lowercase().str.contains(name)
        )

        if min_level is not None:
            cond = cond & (pl.col('minimum_level') >= min_level)
        if max_level is not None:
            cond = cond & (pl.col('minimum_level') <= max_level)

        if rarity is not None:
            cond = cond & (pl.col('display_rarity') == rarity)

        if equipment_type_list is not None:
            cond = cond & (pl.col('equipment_type').is_in(equipment_type_list))

        if usable_job is not None:
            cond = cond & (
                pl.col('usable_job').list.contains('[all]')
                | (pl.col('usable_job').list.contains(usable_job))
            )

        if item_group_name is not None:
            cond = cond & (pl.col('item_group_name') == item_group_name)

        if armor_type is not None:
            cond = cond & (pl.col('armor_type') == armor_type)

        query = self.df.filter(cond)
        if limit is not None:
            query = query.limit(limit)
        rs = query.to_dicts()
        logger.info(f'found {len(rs)} equipments found')
        return rs

    def query_by_id(self, id_: int) -> dict:
        rows = self.df.filter(pl.col('id') == id_).head(1).to_dicts()
        if len(rows) == 0:
            raise EquipmentIdNotFoundException(id_)
        return rows[0]
