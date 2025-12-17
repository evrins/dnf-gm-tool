from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import polars as pl
from loguru import logger

from dnfpkgtool.repo.base_repo import BaseRepo
from dnfpkgtool.repo.skill_repo import SkillRepo
from dnfpkgtool.repo.stackable_repo import StackableRepo

enchant_key_mapping = {
    '[all activestatus resistance]': '所有异常状态抗性',
    '[stuck resistance]': '回避率',
    '[stone resistance]': '石化抗性',
    '[hold resistance]': '束缚抗性',
    '[poison resistance]': '中毒抗性',
    '[slow resistance]': '减速抗性',
    '[fire resistance]': '火属性抗性',
    '[light resistance]': '光属性抗性',
    '[dark resistance]': '暗属性抗性',
    '[all elemental resistance]': '所有属性抗性',
    '[pvp]': 'PVP',
    '[magical defense]': '魔法防御',
    '[physical defense]': '物理防御',
    '[physical critical hit]': '物理暴击率',
    '[magical critical hit]': '魔法暴击率',
    '[equipment physical attack]': '物理攻击力',
    '[equipment magical attack]': '魔法攻击力',
    '[equipment physical defense]': '物理防御',
    '[equipment magical defense]': '魔法防御',
    '[physical attack]': '力量',
    '[magical attack]': '智力',
    '[separate attack]': '独立攻击力',
    '[fire attack]': '火属性强化',
    '[water attack]': '冰属性强化',
    '[light attack]': '光属性强化',
    '[dark attack]': '暗属性强化',
    '[all elemental attack]': '所有属性强化',
    '[attack speed]': '攻击速度',
    '[cast speed]': '释放速度',
    '[move speed]': '移动速度',
    '[HP regen speed]': 'HP 回复速度',
    '[MP regen speed]': 'MP 回复速度',
    '[MP MAX]': 'HP 最大值',
    '[HP MAX]': 'MP 最大值',
    '[elemental property]': '属性攻击',
    '[jump power]': '跳跃力',
    '[all skill item container]': '技能等级提升',
    '[skill levelup]': '技能等级提升',
    '[stuck]': '命中率',
    '[rigidity]': '僵直',
    '[all skill item]': '技能等级提升',
    '[hit recovery]': '硬直',
    '[item aura]': '物品光环',
    'special': '特殊效果',
    # keys to ignore
    '': '',
    '[/enchant index]': '',
}

orb_category_order = {
    '所有异常状态抗性': 10,
    '回避率': 20,
    '石化抗性': 30,
    '束缚抗性': 40,
    '中毒抗性': 50,
    '减速抗性': 60,
    '火属性抗性': 70,
    '光属性抗性': 80,
    '暗属性抗性': 90,
    '所有属性抗性': 100,
    'PVP': 110,
    '魔法防御': 120,
    '物理防御': 130,
    '物理暴击率': 140,
    '魔法暴击率': 150,
    '物理攻击力': 160,
    '魔法攻击力': 170,
    '力量': 180,
    '智力': 190,
    '独立攻击力': 200,
    '火属性强化': 210,
    '冰属性强化': 220,
    '光属性强化': 230,
    '暗属性强化': 240,
    '所有属性强化': 250,
    '攻击速度': 260,
    '释放速度': 270,
    '移动速度': 280,
    'HP 回复速度': 290,
    'MP 回复速度': 300,
    'HP 最大值': 310,
    'MP 最大值': 320,
    '属性攻击': 330,
    '跳跃力': 340,
    '技能等级提升': 390,
    '命中率': 370,
    '僵直': 380,
    '硬直': 400,
    '特殊效果': 410,
    '': 430,
}

enchant_key = '[enchant]'


def transform_job_name(job_name: str) -> str:
    return job_name.replace('[', '').replace(']', '').replace(' ', '').lower()


def render_skills_text(skill_repo: SkillRepo, arr: List[Dict]) -> list[str]:
    res = []
    for it in arr:
        if text := render_skill_text(skill_repo, it):
            res.append(text)
    return res


def render_skill_text(skill_repo: SkillRepo, it: Dict) -> str | None:
    skill = skill_repo.query_by_job_and_id_of_job(
        transform_job_name(it['role']), it['skill_id']
    )
    if skill:
        return f'{skill["name"]} +{it["level_up"]}'
    else:
        return None


# render effect display based on keys
def render_display_effect(enchant: dict, skill_repo: SkillRepo) -> str:
    res = []

    # special effect use stat_desc instead
    if '[if]' in enchant:
        return ''

    for k, v in enchant.items():
        if not v:
            continue

        # ignore keys
        if k in ['display_enchant_category', 'item_aura', 'string_data']:
            continue

        if k == 'elemental_property':
            if v == '[light element]':
                res.append('光')
            elif v == '[fire element]':
                res.append('火')
            elif v == '[water element]':
                res.append('冰')
            elif v == '[dark element]':
                res.append('暗')
            else:
                res.append('未知属性')
        elif k == 'skill_level_up':
            res.extend(render_skills_text(skill_repo, v))
        elif k == 'all_skill_item_container':
            if not v['all_skill_item']['item_grow_type']:
                continue

            lower = v['all_skill_item']['skill_apply_condition']['lower_bound_level']
            upper = v['all_skill_item']['skill_apply_condition']['upper_bound_level']
            level = v['all_skill_item']['skill_apply_condition']['value']
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        elif k == 'all_skill_item':
            if not v['skill_apply_condition']['item_grow_type']:
                continue

            lower = v['skill_apply_condition']['lower_bound_level']
            upper = v['skill_apply_condition']['upper_bound_level']
            level = v['skill_apply_condition']['value']
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        elif k == 'stuck':
            v = abs(v)
            if v < 1:
                res.append(f'+{v:.1}%')
            else:
                res.append(f'+{v}%')
        elif k in ['attack_speed', 'move_speed', 'cast_speed']:
            v = v / 10
            res.append(f'+{v:.1f}%')
        elif k == 'physical_critical_hit' or k == 'magical_critical_hit':
            res.append(f'+{v}%')
        else:
            if isinstance(v, dict):
                print('stop here')
            res.append(f'+{v}')

    return ' '.join(res)


def build_orb_repo_parquet(
    stackable_repo: StackableRepo, skill_repo: SkillRepo, fp: str | Path
):
    orb_list = stackable_repo.query('', stackable_type_list=['[enchant waste]'])
    rs: defaultdict = defaultdict(list)
    for orb in orb_list:
        rs['orb_id'].append(orb['id'])
        rs['orb_name'].append(orb['name'])
        rs['orb_name2'].append(orb['name2'])

        monster_card_id = orb['monster_card_id']
        if not monster_card_id:
            logger.warning(f'monster_card_id not found in {orb["name"]}')
        card = stackable_repo.query_by_id(monster_card_id)
        rs['card_id'].append(card['id'])
        rs['card_name'].append(card['name'])
        rs['card_name2'].append(card['name2'])
        enchant = card['enchant']
        rs['display_enchant_category'].append(enchant['display_enchant_category'])

        display_effect = render_display_effect(enchant, skill_repo)
        rs['display_effect'].append(display_effect)

        apply_parts = card['string_data'][1:]

        rs['apply_parts'].append(apply_parts)

        stat_desc = card['stat_desc']
        if stat_desc:
            stat_desc = stat_desc[0]
            stat_desc.strip()
        rs['stat_desc'].append(stat_desc)

    df = pl.DataFrame(rs)
    df.write_parquet(fp)


class OrbRepo(BaseRepo):
    def query_by_card_id(self, card_id: int) -> dict:
        return self.df.filter(pl.col('card_id') == card_id).limit(1).to_dicts()[0]

    def query_by_display_enchant_category(
        self, display_enchant_category: str
    ) -> List[dict]:
        return (
            self.df.filter(
                pl.col('display_enchant_category').list.contains(
                    display_enchant_category
                )
            )
            .sort(pl.col('orb_id'), descending=False)
            .to_dicts()
        )

    def query_by_display_enchant_category_and_equipment_type(
        self, display_enchant_category: str, equipment_type: str
    ) -> List[dict]:
        return (
            self.df.filter(
                (
                    pl.col('display_enchant_category').list.contains(
                        display_enchant_category
                    )
                )
                & pl.col('apply_parts').list.contains(equipment_type)
            )
            .sort(pl.col('orb_id'), descending=False)
            .to_dicts()
        )
