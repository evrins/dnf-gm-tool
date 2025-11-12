from pathlib import Path
from typing import Dict, List

import polars as pl
from loguru import logger

from config import config
from dnfpkgtool.pvf.pvf_reader import PVFDict
from dnfpkgtool.repo import MappingElementLocation, remapping_pvf_dict
from dnfpkgtool.repo.base_repo import BaseRepo
from util import time_it


def map_armor_type(d: dict[str, str]) -> str:
    et = d['equipment_type']
    ign = d['item_group_name']
    if not ign:
        return ''
    if et in ['[coat]', '[waist]', '[shoulder]', '[pants]', '[shoes]']:
        parts = ign.split(' ')
        if len(parts) != 2:
            raise ValueError('invalid item group name')
        return parts[0]
    return ''


equipment_mapping = {
    '': '契约效果',
    '[artifact blue]': '蓝色 宠物装备',
    '[artifact green]': '绿色 宠物装备',
    '[artifact red]': '红色 宠物装备',
    '[aurora avatar]': '光环',
    '[hair avatar]': '头部装扮',
    '[hat avatar]': '帽子装扮',
    '[face avatar]': '脸部装扮',
    '[breast avatar]': '胸部装扮',
    '[coat avatar]': '上衣装扮',
    '[skin avatar]': '皮肤装扮',
    '[waist avatar]': '腰部装扮',
    '[pants avatar]': '下装装扮',
    '[shoes avatar]': '脚部装扮',
    '[coat]': '上衣',
    '[waist]': '腰带',
    '[pants]': '下装',
    '[shoulder]': '头肩',
    '[shoes]': '鞋子',
    '[magic stone]': '魔法石',
    '[support]': '辅助装备',
    '[creature]': '宠物',
    '[title name]': '称号',
    '[weapon]': '武器',
    '[wrist]': '手镯',
    '[amulet]': '项链',
    '[ring]': '戒指',
}

weapon_mapping = {
    '短剑': 'ssword',
    '太刀': 'katana',
    '巨剑': 'lswd',
    '钝器': 'club',
    '光剑': 'beamswd',
    '手套': 'knuckle',
    '臂铠': 'gauntlet',
    '爪': 'claw',
    '拳套': 'bglove',
    '东方棍': 'tonfa',
    '自动手枪': 'automatic',
    '手弩': 'bowgun',
    '左轮': 'revolver',
    '步枪': 'musket',
    '手炮': 'hcannon',
    '法杖': 'staff',
    '魔杖': 'rod',
    '棍棒': 'pole',
    '矛': 'spear',
    '扫把': 'broom',
    '十字架': 'cross',
    '镰刀': 'scythe',
    '念珠': 'rosary',
    '图腾': 'totem',
    '战斧': 'axe',
    '手杖': 'wand',
    '匕首': 'dagger',
    '双剑': 'twinswd',
}

weapon_mapping = {v: k for k, v in weapon_mapping.items()}

job_name_mapping = {
    '[all]': '全部职业',
    '[swordman]': '鬼剑士',
    '[fighter]': '格斗家',
    '[at fighter]': '格斗家-男',
    '[gunner]': '神枪手',
    '[at gunner]': '神枪手-女',
    '[mage]': '魔法师',
    '[at mage]': '魔法师-男',
    '[priest]': '圣职者',
    '[thief]': '暗夜使者',
    '[demonic swordman]': '黑暗武士',
    '[creator mage]': '缔造者',
}


def map_display_equipment_type(d: Dict[str, str]) -> str:
    equipment_type = d['equipment_type']
    item_group_name = d['item_group_name']
    if equipment_type == '[weapon]':
        return weapon_mapping[item_group_name]
    else:
        return equipment_mapping[equipment_type]


def map_display_rarity(d: dict[str, str | int]) -> str:
    id_ = d['id']
    name = d['name']
    rarity = d['rarity']
    item_category = d['item_category']

    name = name.strip()
    if name.startswith('传承'):
        return '传承'

    item_category = item_category.strip()
    if item_category == 'boss drop':
        return '领主神器'

    if rarity == 0:
        return '普通'
    elif rarity == 1:
        return '高级'
    elif rarity == 2:
        return '稀有'
    elif rarity == 3:
        return '神器'
    elif rarity == 4:
        return '史诗'
    elif rarity == 5:
        return '勇者'

    raise ValueError(f'{id_} unknown rarity {rarity}')


def map_display_usable_job(usable_job: List[str]) -> str:
    return ','.join([job_name_mapping[it] for it in usable_job])


def build_equipment_repo_parquet(pvf_dict: PVFDict, fp: str | Path):
    mappings = [
        ('level', '[minimum level]', 0, MappingElementLocation.First),
        ('rarity', '[rarity]', 0, MappingElementLocation.First),
        ('equipment_type', '[equipment type]', '', MappingElementLocation.First),
        ('sub_equipment_type', '[equipment type]', 0, MappingElementLocation.Second),
        ('item_group_name', '[item group name]', '', MappingElementLocation.First),
        ('item_category', '[item category]', '', MappingElementLocation.First),
        ('usable_job', '[usable job]', [], MappingElementLocation.All),
        ('physical_attack', '[physical attack]', 0, MappingElementLocation.First),
        ('magical_attack', '[magical attack]', 0, MappingElementLocation.First),
        ('physical_defense', '[physical defense]', 0, MappingElementLocation.First),
        ('magical_defense', '[magical defense]', 0, MappingElementLocation.First),
        (
            'physical_critical_hit',
            '[physical critical hit]',
            0.0,
            MappingElementLocation.First,
        ),
        (
            'magical_critical_hit',
            '[magical critical hit]',
            0.0,
            MappingElementLocation.First,
        ),
        (
            'all_elemental_attack',
            '[all elemental attack]',
            0,
            MappingElementLocation.First,
        ),
        ('attack_speed', '[attack speed]', 0, MappingElementLocation.First),
        ('cast_speed', '[cast speed]', 0, MappingElementLocation.First),
        ('move_speed', '[move speed]', 0, MappingElementLocation.First),
        (
            'room_list_move_speed_rate',
            '[room list move speed rate]',
            0.0,
            MappingElementLocation.First,
        ),
        ('mp_max_rate', '[MP MAX rate]', 0.0, MappingElementLocation.First),
        ('set_name', '[set name]', '', MappingElementLocation.First),
        ('set_item', '[set item]', [], MappingElementLocation.All),
        ('durability', '[durability]', 0, MappingElementLocation.First),
        ('sub_type', '[sub type]', 0, MappingElementLocation.First),
    ]
    df = remapping_pvf_dict(pvf_dict, mappings)
    df = pl.DataFrame(df)
    df = df.with_columns(
        pl.struct(['id', 'equipment_type', 'item_group_name'])
        .map_elements(map_armor_type, return_dtype=pl.String)
        .alias('armor_type'),
        pl.struct(['equipment_type', 'item_group_name'])
        .map_elements(map_display_equipment_type)
        .alias('display_equipment_type'),
        pl.struct(['id', 'name', 'rarity', 'item_category'])
        .map_elements(map_display_rarity, return_dtype=pl.String)
        .alias('display_rarity'),
        pl.col('usable_job')
        .map_elements(map_display_usable_job, return_dtype=pl.String)
        .alias('display_usable_job'),
        pl.col('attack_speed') // 10,
        pl.col('cast_speed') // 10,
        pl.col('move_speed') // 10,
        pl.col('room_list_move_speed_rate') * 100,
        pl.col('mp_max_rate').cast(pl.Int64),
    )

    df = df.drop(['item_category'])
    df.write_parquet(fp)


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
            cond = cond & (pl.col('level') >= min_level)
        if max_level is not None:
            cond = cond & (pl.col('level') <= max_level)

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


def get_equipment_repo() -> EquipmentRepo:
    fp = config.get_equipment_parquet_file_path()
    return EquipmentRepo(fp)
