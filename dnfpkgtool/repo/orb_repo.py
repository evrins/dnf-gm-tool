import json
from collections import defaultdict
from pathlib import Path
from typing import List

import polars as pl

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


def render_skills_text(skill_repo: SkillRepo, arr: list) -> list[str]:
    res = []
    for i in range(0, len(arr), 3):
        res.append(render_skill_text(skill_repo, arr[i : i + 3]))
    return res


def render_skill_text(skill_repo: SkillRepo, arr: list) -> str:
    skill = skill_repo.query_by_job_and_id_of_job(transform_job_name(arr[0]), arr[1])
    return f'{skill["name"]} +{arr[2]}'


# render effect display based on keys
def render_display_effect(enchant: dict, skill_repo: SkillRepo) -> str:
    res = []

    # special effect use stat_desc instead
    if '[if]' in enchant:
        return ''

    for k, v in enchant.items():
        if k == '[elemental property]':
            if v[0] == '[light element]':
                res.append('光')
            elif v[0] == '[fire element]':
                res.append('火')
            elif v[0] == '[water element]':
                res.append('冰')
            elif v[0] == '[dark element]':
                res.append('暗')
            else:
                res.append('未知属性')
        # skip empty key
        elif k == '' or k == '[/enchant index]':
            continue
        elif k == '[skill levelup]':
            res.extend(render_skills_text(skill_repo, v))
        # ignore this key
        elif k == '[all skill item container]':
            lower = v['[all skill item]']['[skill apply condition]'][
                '[lower bound level]'
            ][0]
            upper = v['[all skill item]']['[skill apply condition]'][
                '[upper bound level]'
            ][0]
            level = v['[all skill item]']['[skill apply condition]']['[value]'][0]
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        elif k == '[all skill item]':
            lower = v['[skill apply condition]']['[lower bound level]'][0]
            upper = v['[skill apply condition]']['[upper bound level]'][0]
            level = v['[skill apply condition]']['[value]'][0]
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        elif k == '[stuck]':
            v = abs(v[0])
            if v < 1:
                res.append(f'+{v:.1}%')
            else:
                res.append(f'+{v}%')
        elif k in ['[attack speed]', '[move speed]', '[cast speed]']:
            v = v[0]
            v = v / 10
            res.append(f'+{v:.1f}%')
        elif k == '[physical critical hit]' or k == '[magical critical hit]':
            res.append(f'+{v[0]}%')
        else:
            if len(v) == 0:
                print('empty values')
            if isinstance(v, dict):
                print('stop here')
            res.append(f'+{v[0]}')

    return ' '.join(res)


def build_orb_repo_parquet(
    stackable_repo: StackableRepo, skill_repo: SkillRepo, fp: str | Path
):
    orb_list = stackable_repo.query('', stackable_type_list=['[enchant waste]'])
    rs: defaultdict = defaultdict(list)
    for orb in orb_list:
        orb_d = json.loads(orb['json'])
        rs['orb_id'].append(orb['id'])
        rs['orb_name'].append(orb['name'])
        rs['orb_name2'].append(orb['name2'])

        monster_card_id = orb_d['[monster card id]'][0]
        if not monster_card_id:
            print(f'[monster card id] not found in {orb["name"]}')
        card = stackable_repo.query_by_id(monster_card_id)
        rs['card_id'].append(card['id'])
        rs['card_name'].append(card['name'])
        rs['card_name2'].append(card['name2'])
        card_d = json.loads(card['json'])
        enchant = card_d[enchant_key]
        enchant_category = list(enchant.keys())
        rs['enchant'].append(json.dumps(enchant))
        if '[if]' in enchant_category or '[then]' in enchant_category:
            enchant_category = ['special']
        rs['enchant_category'].append(enchant_category)

        rs['display_enchant_category'].append(
            list(
                filter(
                    lambda it: it,
                    map(lambda it: enchant_key_mapping[it], enchant_category),
                )
            )
        )

        display_effect = render_display_effect(enchant, skill_repo)
        rs['display_effect'].append(display_effect)

        apply_parts = card_d['[string data]'][1:]

        rs['apply_parts'].append(apply_parts)

        stat_desc = card_d.get('[stat desc]', '')
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


