from pathlib import Path
from typing import List

import polars as pl
from loguru import logger

from config import config
from dnfpkgtool.pvf.pvf_reader import PVFDict
from dnfpkgtool.repo import MappingElementLocation, remapping_pvf_dict
from dnfpkgtool.repo.base_repo import BaseRepo
from ui.components.stackable_search.vars import item_rarity_list

stackable_mapping = {
    '[avatar emblem]': '时装徽章',
    '[booster random]': '礼包',
    '[booster selection]': '礼包',
    '[booster]': '礼包',
    '[cera booster]': '礼包',
    '[cera package]': '礼包',
    '[usable cera package]': '礼包',
    '[upgrade limit cube]': '礼包',
    '[contract]': '契约',
    '[creature expitem]': '宠物经验道具',
    '[creature]': '宠物',
    '[feed]': '宠物道具',
    '[disguise random]': '变身道具',
    '[disguise]': '变身道具',
    '[dye]': '染色剂',
    '[enchant waste]': '附魔宝珠',
    '[expert town potion]': '秘药',
    '[global effect]': '频道道具',
    '[material expert job]': '副职业',
    '[material]': '材料',
    '[etc]': '其他',
    '[legacy]': '其他',
    '[multi upgradable legacy bonus cera]': '其他',
    '[multi upgradable legacy]': '其他',
    '[stackable legacy]': '其他',
    '[only effect]': '其他',
    '[town and dungeon]': '其他',
    '[unlimited town and dungeon]': '其他',
    '[unlimited etc]': '其他',
    '[upgradable legacy]': '袖珍罐',
    '[quest receive]': '悬赏令',
    '[quest]': '任务道具',
    '[recipe]': '设计图',
    '[set]': '地雷',
    '[teleport potion]': '瞬间移动药剂',
    '[throw]': '投掷物',
    '[waste]': '消耗品',
    '[unlimited waste]': '消耗品',
}


def map_stackable_type(d: dict[str, str]) -> str:
    item_category = d['item_category']
    if item_category == 'monster card':
        return '卡片'
    stackable_type = d['stackable_type']
    return stackable_mapping[stackable_type]


def map_display_rarity(rarity: int) -> str:
    display_rarity = item_rarity_list[rarity]
    return display_rarity


def build_stackable_repo_parquet(pvf_dict: PVFDict, fp: str | Path):
    mappings = [
        ('level', '[minimum level]', 0, MappingElementLocation.First),
        ('rarity', '[rarity]', 0, MappingElementLocation.First),
        ('stackable_type', '[stackable type]', '', MappingElementLocation.First),
        ('sub_stackable_type', '[stackable type]', 0, MappingElementLocation.Second),
        ('item_group_name', '[item group name]', '', MappingElementLocation.First),
        ('item_category', '[item category]', '', MappingElementLocation.First),
        ('stack_limit', '[stack limit]', 0, MappingElementLocation.First),
        ('usable_job', '[usable job]', [], MappingElementLocation.All),
    ]

    df = remapping_pvf_dict(pvf_dict, mappings)
    df = pl.DataFrame(df)
    df = df.with_columns(
        pl.struct(['stackable_type', 'item_category'])
        .map_elements(map_stackable_type, return_dtype=pl.String)
        .alias('display_stackable_type'),
        pl.col('rarity')
        .map_elements(map_display_rarity, return_dtype=pl.String)
        .alias('display_rarity'),
    )
    df.write_parquet(fp)


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
            cond = cond & (pl.col('level') >= min_level)
        if max_level is not None:
            cond = cond & (pl.col('level') <= max_level)
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


def get_stackable_repo() -> StackableRepo:
    fp = config.get_stackable_parquet_file_path()
    return StackableRepo(fp)
