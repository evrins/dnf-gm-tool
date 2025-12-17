from typing import List

import polars as pl
from loguru import logger

from dnfpkgtool.repo.base_repo import BaseRepo


class StackableIdNotFoundException(Exception):
    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__('Stackable ID not found')

    def __str__(self):
        return f'Stackable ID not found: {self.item_id}'


class StackableRepo(BaseRepo):
    def query(
        self,
        name: str,
        stackable_type_list: list[str] | None = None,
        item_category_list: list[str] | None = None,
        min_level: int | None = None,
        max_level: int | None = None,
        display_rarity: str | None = None,
        item_type: str | None = None,
        limit: int | None = None,
    ) -> List[dict]:
        logger.info(
            f'query with name {name} stackable_type_list {stackable_type_list} item_category_list {item_category_list} min_level {min_level} max_level {max_level} display_rarity {display_rarity} item_type {item_type}'
        )
        name = name.lower()
        cond = pl.col('name').str.contains(name) | pl.col(
            'name2'
        ).str.to_lowercase().str.contains(name)

        if stackable_type_list is not None:
            cond = cond & (pl.col('stackable_type').is_in(stackable_type_list))
        if item_category_list is not None:
            cond = cond & (pl.col('item_category').is_in(item_category_list))
        if min_level is not None:
            cond = cond & (pl.col('minimum_level') >= min_level)
        if max_level is not None:
            cond = cond & (pl.col('minimum_level') <= max_level)
        if display_rarity is not None:
            cond = cond & (pl.col('display_rarity') == display_rarity)

        if item_type is not None:
            cond = cond & (pl.col('item_type') == item_type)

        query = self.df.filter(cond).select('*')
        if limit is not None:
            query = query.limit(limit)

        return query.to_dicts()

    def query_by_id(self, id_: int) -> dict:
        rows = self.df.filter(pl.col('id') == id_).limit(1).to_dicts()
        if len(rows) == 0:
            raise StackableIdNotFoundException(id_)
        return rows[0]
