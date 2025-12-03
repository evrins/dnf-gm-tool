from typing import List

from pydantic import ConfigDict

from dnfpkgtool.pvf.entity.all_skill_item import AllSkillItem
from dnfpkgtool.pvf.entity.avatar_select_ability import AvatarSelectAbility
from dnfpkgtool.pvf.entity.emancipate import Emancipate
from dnfpkgtool.pvf.entity.piece_set_ability import PieceSetAbility
from dnfpkgtool.pvf.entity.set_ability import SetAbility
from dnfpkgtool.pvf.entity.stat_property import StatProperty


class Equipment(StatProperty):
    model_config = ConfigDict(validate_assignment=True)

    id: int = 0
    name: str = ''
    name2: str = ''
    grade: int = 0
    rarity: int = 0
    usable_job: List[str] = []
    minimum_level: int = 0
    maximum_level: int = 0
    price: int = 0
    repair_price: int = 0
    value: int = 0
    equipment_type: str = ''
    sub_type: int = 0
    durability: int = 0
    weight: int = 0
    item_group_name: str = ''
    cool_time: int = 0
    set_name: str = ''
    set_item: List[int] = []
    enable_dye: List[int] = []
    part_set_index: int = 0
    avatar_select_ability: List[AvatarSelectAbility] = []
    item_category: List[str] = []
    set_ability: SetAbility | None = None
    set_item_master: int = 0
    all_skill_item: List[AllSkillItem] = []
    push_aside: int = 0

    # creature start
    int_data: List[int] = []
    creature_species: int = 0
    output_index: int = 0
    cash: int = 0
    creature_min_level: int = 0
    creature_skill_consume_mp_rate: float = 0
    creature_skill_over_charge_time_rate: float = 0
    creature_experience_amount_rate: float = 0
    creature_physical_critical_hit: float = 0
    creature_magical_critical_hit: float = 0
    creature_stuck: float = 0

    # 远古装备
    emancipate: Emancipate | None = None

    # 决斗装备
    minimum_rank: int = 0
    usable_world: List[str] = []

    # 副职业
    prof_compound_rate: int = 0
    prof_additional_gain_exp: List[int] = []
    prof_result_variation: List[int] = []
    prof_disjoint_result_variation: List[int] = []
    prof_material_variation: List[int] = []

    # 光环
    aurora_avatar: int = 0

    # 时装
    clear_avatar: int = 0

    special_monster_drop: int = 0
    difficulty_for_extra_drop: List[str] = []
    dungeon_type_for_extra_drop: List[str] = []

    piece_set_ability: List[PieceSetAbility] = []
