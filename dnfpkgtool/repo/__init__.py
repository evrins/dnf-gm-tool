import enum
import json
from typing import Dict, List, Tuple

from dnfpkgtool.pvf.pvf_reader import PVFDict


def extract_common_field(d: dict) -> dict:
    res = {}
    name = d.get('[name]', [])
    if name:
        name = name[0]
    name2 = d.get('[name2]', [])
    if name2:
        name2 = name2[0]
    else:
        name2 = ''

    if not name:
        name = name2

    res['name'] = name
    res['name2'] = name2

    level = d.get('[minimum level]', [])
    if level:
        level = level[0]
    else:
        level = 0

    res['level'] = level

    rarity = d.get('[rarity]', [])
    if rarity:
        rarity = rarity[0]
    else:
        rarity = 0

    res['rarity'] = rarity

    return res


class MappingElementLocation(enum.Enum):
    First = 1
    Second = 2
    All = 3
    Join = 4


type MappingConfig = Tuple[str, str, any, MappingElementLocation]


def remapping_pvf_dict(
    pvf_dict: PVFDict, mappings: List[MappingConfig], separate: str = '-'
) -> dict[str, List[any]]:
    res = {
        'id': [],
        'name': [],
        'name2': [],
        'json': [],
    }

    for k, *_ in mappings:
        res[k] = []

    for k, v in pvf_dict.items():
        res['id'].append(k)

        name = v.get('[name]', [])
        if name:
            name = name[0]
        name2 = v.get('[name2]', [])
        if name2:
            name2 = name2[0]
        else:
            name2 = ''

        if not name:
            name = name2

        res['name'].append(name)
        res['name2'].append(name2)

        res['json'].append(json.dumps(v, ensure_ascii=False))

        for k1, k2, default, mpl in mappings:
            v2 = v.get(k2, [])
            if v2:
                if mpl == MappingElementLocation.First:
                    v2 = v2[0]
                elif mpl == MappingElementLocation.Second:
                    v2 = v2[1]
                elif mpl == MappingElementLocation.Join:
                    v2 = separate.join(v2)
                else:
                    v2 = v2
            else:
                v2 = default
            res[k1].append(v2)

    return res


def remapping_pvf_list(
    pvf_list: List[Dict[str, List[any]]],
    mappings: List[MappingConfig],
    separate: str = '-',
) -> Dict[str, List[any]]:
    res = {}

    for k, *_ in mappings:
        res[k] = []

    for it in pvf_list:
        for target_key, source_key, default, mpl in mappings:
            v2 = it.get(source_key, [])
            if v2:
                if mpl == MappingElementLocation.First:
                    v2 = v2[0]
                elif mpl == MappingElementLocation.Second:
                    v2 = v2[1]
                elif mpl == MappingElementLocation.Join:
                    v2 = separate.join(v2)
                else:
                    v2 = v2
            else:
                v2 = default
            res[target_key].append(v2)

    return res
