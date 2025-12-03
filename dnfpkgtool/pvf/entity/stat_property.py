from typing import List

from pydantic import BaseModel, ConfigDict

from dnfpkgtool.pvf.entity.item_aura import ItemAura
from dnfpkgtool.pvf.entity.skill_levelup import SkillLevelUp


class StatProperty(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    physical_attack: int | None = None
    physical_defense: int | None = None
    magical_attack: int | None = None
    magical_defense: int | None = None
    separate_attack: int | None = None
    hp_max: int | None = None
    mp_max: int | None = None
    inventory_limit: int | None = None
    hp_regen_speed: int | None = None
    hp_regen_speed_rate: int | None = None
    mp_regen_speed: int | None = None
    mp_regen_speed_rate: int | None = None
    move_speed: int | None = None
    attack_speed: int | None = None
    cast_speed: int | None = None
    stuck_resistance: int | None = None
    stuck: float = 0
    rigidity: float = 0
    all_elemental_attack: int | None = None
    all_elemental_resistance: int | None = None

    stun_resistance: int | None = None
    piercing_resistance: int | None = None
    freeze_resistance: int | None = None
    confuse_resistance: int | None = None
    poison_resistance: int | None = None
    stone_resistance: int | None = None
    blind_resistance: int | None = None
    curse_resistance: int | None = None
    bleeding_resistance: int | None = None
    lightning_resistance: int | None = None
    burn_resistance: int | None = None
    sleep_resistance: int | None = None
    slow_resistance: int | None = None
    hold_resistance: int | None = None

    dark_attack: int | None = None
    light_attack: int | None = None
    fire_attack: int | None = None
    water_attack: int | None = None

    dark_resistance: int | None = None
    light_resistance: int | None = None
    fire_resistance: int | None = None
    water_resistance: int | None = None

    all_activestatus_resistance: int | None = None
    room_list_move_speed_rate: float | None = None
    parameter_basic_explain: str | None = None
    parameter_detail_explain: str | None = None
    fullset_explain: str | None = None
    fullset_basic_explain: str | None = None
    fullset_detail_explain: str | None = None
    jump_power: int | None = None
    physical_critical_hit: float | None = None
    magical_critical_hit: float | None = None

    skill_data_up: None = None
    skill_level_up: List[SkillLevelUp] = []
    item_aura: List[ItemAura] = []

    equipment_physical_attack: int | None = None
    equipment_magical_attack: int | None = None
    equipment_physical_defense: int | None = None
    equipment_magical_defense: int | None = None
    anti_evil: int | None = None
    hit_recovery: int | None = None

    flavor_text: str | None = None
    explain: str | None = None
    basic_explain: str | None = None
    detail_explain: str | None = None

    elemental_property: str | None = None

    creature_magical_attack: int | None = None
    creature_physical_attack: int | None = None
    creature_skill_charge_time_rate: float | None = None

    hp_max_rate: float | None = 0
    mp_max_rate: float | None = 0

    lift_up: int | None = None
