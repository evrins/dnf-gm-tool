from typing import List

from pydantic import BaseModel

from dnfpkgtool.pvf.entity.item_aura import ItemAura
from dnfpkgtool.pvf.entity.skill_levelup import SkillLevelUp


class StatProperty(BaseModel):
    physical_attack: int = 0
    physical_defense: int = 0
    magical_attack: int = 0
    magical_defense: int = 0
    separate_attack: int = 0
    hp_max: int = 0
    mp_max: int = 0
    inventory_limit: int = 0
    hp_regen_speed: int = 0
    mp_regen_speed: int = 0
    move_speed: int = 0
    attack_speed: int = 0
    cast_speed: int = 0
    stuck_resistance: int = 0
    stuck: float = 0
    all_elemental_attack: int = 0
    all_elemental_resistance: int = 0

    stun_resistance: int = 0

    dark_attack: int = 0
    light_attack: int = 0
    fire_attack: int = 0
    water_attack: int = 0

    dark_resistance: int = 0
    light_resistance: int = 0
    fire_resistance: int = 0
    water_resistance: int = 0

    all_activestatus_resistance: int = 0
    room_list_move_speed_rate: float = 0
    parameter_basic_explain: str = ''
    parameter_detail_explain: str = ''
    fullset_explain: str = ''
    jump_power: int = 0
    physical_critical_hit: int = 0
    magical_critical_hit: int = 0

    skill_data_up: None = None
    skill_level_up: List[SkillLevelUp] = []
    item_aura: List[ItemAura] = []

    equipment_physical_attack: int = 0
    equipment_magical_attack: int = 0
    equipment_physical_defense: int = 0
    equipment_magical_defense: int = 0
    anti_evil: int = 0
    hit_recovery: int = 0