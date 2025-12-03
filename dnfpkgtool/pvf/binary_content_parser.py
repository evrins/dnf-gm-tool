from enum import Enum
from typing import Callable, List

from dnfpkgtool.pvf.entity.all_skill_item import AllSkillItem
from dnfpkgtool.pvf.entity.avatar_select_ability import AvatarSelectAbility
from dnfpkgtool.pvf.entity.binary_content import BinaryContent, BinaryItem
from dnfpkgtool.pvf.entity.emancipate import Emancipate
from dnfpkgtool.pvf.entity.equipment import Equipment
from dnfpkgtool.pvf.entity.item_aura import ItemAura
from dnfpkgtool.pvf.entity.piece_set import PieceSet
from dnfpkgtool.pvf.entity.piece_set_ability import PieceSetAbility
from dnfpkgtool.pvf.entity.quest import Quest
from dnfpkgtool.pvf.entity.set_ability import SetAbility
from dnfpkgtool.pvf.entity.skill_apply_condition import SkillApplyCondition
from dnfpkgtool.pvf.entity.skill_levelup import SkillLevelUp


class ReturnType(Enum):
    Single = 1
    List = 2
    NoneValue = 3


type parse_function_type = Callable[[], object]


class BinaryContentParser:
    def __init__(self, bc: BinaryContent):
        super().__init__()

        self.bc: BinaryContent = bc
        self.total: int = len(bc)
        self.idx: int = 0

        self.parse_function_map = {
            '[set name]': ('set_name', ReturnType.Single, self.parse_next_one),
            '[physical attack]': (
                'physical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[physical defense]': (
                'physical_defense',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[magical attack]': (
                'magical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[magical defense]': (
                'magical_defense',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[separate attack]': (
                'separate_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[HP MAX]': ('hp_max', ReturnType.Single, self.parse_next_one),
            '[MP MAX]': ('mp_max', ReturnType.Single, self.parse_next_one),
            '[HP MAX rate]': ('hp_max_rate', ReturnType.Single, self.parse_next_one),
            '[MP MAX rate]': ('mp_max_rate', ReturnType.Single, self.parse_next_one),
            '[inventory limit]': (
                'inventory_limit',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[HP regen speed]': (
                'hp_regen_speed',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[MP regen speed]': (
                'mp_regen_speed',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[move speed]': ('move_speed', ReturnType.Single, self.parse_next_one),
            '[attack speed]': ('attack_speed', ReturnType.Single, self.parse_next_one),
            '[cast speed]': ('cast_speed', ReturnType.Single, self.parse_next_one),
            '[stuck resistance]': (
                'stuck_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[stuck]': ('stuck', ReturnType.Single, self.parse_next_one),
            '[stun resistance]': (
                'stun_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[piercing resistance]': (
                'piercing_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[freeze resistance]': (
                'freeze_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[confuse resistance]': (
                'confuse_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[poison resistance]': (
                'poison_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[blind resistance]': (
                'blind_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[stone resistance]': (
                'stone_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[curse resistance]': (
                'curse_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[bleeding resistance]': (
                'bleeding_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[lightning resistance]': (
                'lightning_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[burn resistance]': (
                'burn_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[sleep resistance]': (
                'sleep_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[slow resistance]': (
                'slow_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[hold resistance]': (
                'hold_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[all elemental attack]': (
                'all_elemental_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[all elemental resistance]': (
                'all_elemental_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[all activestatus resistance]': (
                'all_activestatus_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[room list move speed rate]': (
                'room_list_move_speed_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[parameter basic explain]': (
                'parameter_basic_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[parameter detail explain]': (
                'parameter_detail_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[fullset explain]': (
                'fullset_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[jump power]': ('jump_power', ReturnType.Single, self.parse_next_one),
            '[physical critical hit]': (
                'physical_critical_hit',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[magical critical hit]': (
                'magical_critical_hit',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[equipment physical attack]': (
                'equipment_physical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[equipment magical attack]': (
                'equipment_magical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[equipment physical defense]': (
                'equipment_physical_defense',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[equipment magical defense]': (
                'equipment_magical_defense',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[dark attack]': ('dark_attack', ReturnType.Single, self.parse_next_one),
            '[light attack]': ('light_attack', ReturnType.Single, self.parse_next_one),
            '[fire attack]': ('fire_attack', ReturnType.Single, self.parse_next_one),
            '[water attack]': ('water_attack', ReturnType.Single, self.parse_next_one),
            '[dark resistance]': (
                'dark_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[light resistance]': (
                'light_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[fire resistance]': (
                'fire_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[water resistance]': (
                'water_resistance',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[anti evil]': ('anti_evil', ReturnType.Single, self.parse_next_one),
            '[hit recovery]': ('hit_recovery', ReturnType.Single, self.parse_next_one),
            '[item aura]': ('item_aura', ReturnType.List, self.parse_item_aura),
            '[if]': ('-', ReturnType.NoneValue, self.skip_until('[/if]')),
            '[then]': ('-', ReturnType.NoneValue, self.skip_until('[/then]')),
            '[skill data up]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/skill data up]'),
            ),
            '[multiple then]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/multiple then]'),
            ),
            '[all skill item container]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/all skill item container]'),
            ),
            '[skill levelup]': (
                'skill_level_up',
                ReturnType.Single,
                self.parse_skill_level_up,
            ),
            '[piece set]': ('piece_set', ReturnType.Single, self.parse_piece_set),
            '[piece set ability]': (
                'piece_set_ability',
                ReturnType.List,
                self.parse_piece_set_ability,
            ),
            # quest
            '[grade]': ('grade', ReturnType.Single, self.parse_next_one),
            '[difficulty]': ('difficulty', ReturnType.Single, self.parse_next_one),
            '[gold multiple]': (
                'gold_multiple',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[npc index]': ('npc_index', ReturnType.Single, self.parse_next_one),
            '[complete npc index]': (
                'complete_npc_index',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[job]': ('job', ReturnType.Single, self.parse_next_one),
            '[grow type]': ('grow_type', ReturnType.Single, self.parse_next_one),
            '[level]': ('level', ReturnType.Single, self.parse_next_n(2)),
            '[pre required quest]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/pre required quest]'),
            ),
            '[type]': ('quest_type', ReturnType.Single, self.parse_next_one),
            '[sub type]': ('sub_type', ReturnType.Single, self.parse_next_one),
            '[int data]': (
                'int_data',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[reward type]': ('reward_type', ReturnType.Single, self.parse_next_one),
            '[reward int data]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/reward int data]'),
            ),
            '[reward selection int data]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/reward selection int data]'),
            ),
            '[name]': ('name', ReturnType.Single, self.parse_next_one),
            '[depend message]': (
                'depend_message',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[condition message]': (
                'condition_message',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[solve message]': (
                'solve_message',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[monster reward item]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/monster reward item]'),
            ),
            '[quest point]': ('quest_point', ReturnType.Single, self.parse_next_one),
            '[dungeon info]': (
                'dungeon_info',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[relation quest]': (
                'relation_quest',
                ReturnType.Single,
                self.parse_until_segment,
            ),
            '[enemy reward item]': (
                'enemy_reward_item',
                ReturnType.NoneValue,
                self.skip_until('[/enemy reward item]'),
            ),
            '[dialog]': ('dialog', ReturnType.NoneValue, self.skip_until('[/dialog]')),
            '[depend give item]': (
                'depend_give_item',
                ReturnType.NoneValue,
                self.skip_until('[/depend give item]'),
            ),
            '[substitutive names]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/substitutive names]'),
            ),
            '[target character]': (
                'target_character',
                ReturnType.NoneValue,
                self.skip_until('[/target character]'),
            ),
            '[clear reward item]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/clear reward item]'),
            ),
            '[collision quest]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/collision quest]'),
            ),
            '[limit dungeon index]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/limit dungeon index]'),
            ),
            '[check count]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/check count]'),
            ),
            '[condition data]': (
                'condition_data',
                ReturnType.NoneValue,
                self.skip_until('[/condition data]'),
            ),
            '[string data]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/string data]'),
            ),
            '[schedule]': ('-', ReturnType.NoneValue, self.skip_until('[/schedule]')),
            # equipment
            '[name2]': ('name2', ReturnType.Single, self.parse_next_one),
            '[rarity]': ('rarity', ReturnType.Single, self.parse_next_one),
            '[usable job]': (
                'usable_job',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[minimum level]': (
                'minimum_level',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[maximum level]': (
                'maximum_level',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[level linear ability]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/level linear ability]'),
            ),
            '[price]': ('price', ReturnType.Single, self.parse_next_one),
            '[repair price]': ('repair_price', ReturnType.Single, self.parse_next_one),
            '[value]': ('value', ReturnType.Single, self.parse_next_one),
            '[equipment type]': (
                'equipment_type',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[durability]': ('durability', ReturnType.Single, self.parse_next_one),
            '[weight]': ('weight', ReturnType.Single, self.parse_next_one),
            '[item group name]': (
                'item_group_name',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[cool time]': ('cool_time', ReturnType.Single, self.parse_next_one),
            '[basic explain]': (
                'basic_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[detail explain]': (
                'detail_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[flavor text]': ('flavor_text', ReturnType.Single, self.parse_next_one),
            '[set item]': (
                'set_item',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[set ability]': ('set_ability', ReturnType.Single, self.parse_set_ability),
            '[fullset basic explain]': (
                'fullset_basic_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[fullset detail explain]': (
                'fullset_detail_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[routing priority]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/routing priority]'),
            ),
            '[explain]': ('explain', ReturnType.Single, self.parse_next_one),
            '[custom animation]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/custom animation]'),
            ),
            '[enable dye]': ('enable_dye', ReturnType.Single, self.parse_until_segment),
            '[part set index]': (
                'part_set_index',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[set item master]': (
                'set_item_master',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[avatar type select]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/avatar type select]'),
            ),
            '[avatar select ability]': (
                'avatar_select_ability',
                ReturnType.Single,
                self.parse_avatar_select_ability,
            ),
            '[item category]': (
                'item_category',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[impossible contents]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/impossible contents]'),
            ),
            '[pvp]': ('-', ReturnType.NoneValue, self.skip_until('[/pvp]')),
            '[rebirth]': ('-', ReturnType.NoneValue, self.skip_until('[/rebirth]')),
            '[elemental property]': (
                'elemental_property',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[all skill item]': (
                'all_skill_item',
                ReturnType.List,
                self.parse_all_skill_item,
            ),
            '[skill apply condition]': (
                'skill_apply_condition',
                ReturnType.Single,
                self.parse_skill_apply_condition,
            ),
            '[extra condition]': (
                'extra_condition',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[item growtype]': (
                'item_grow_type',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[skill group]': ('skill_group', ReturnType.Single, self.parse_next_one),
            '[lower bound level]': (
                'lower_bound_level',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[upper bound level]': (
                'upper_bound_level',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[skill phase]': ('skill_phase', ReturnType.Single, self.parse_next_one),
            '[push aside]': ('push_aside', ReturnType.Single, self.parse_next_one),
            '[MP regen speed rate]': (
                'mp_regen_speed_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[HP regen speed rate]': (
                'hp_regen_speed_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature magical attack]': (
                'creature_magical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature physical attack]': (
                'creature_physical_attack',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature skill charge time rate]': (
                'creature_skill_charge_time_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[custom wav]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/custom wav]'),
            ),
            '[creature species]': (
                'creature_species',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[output index]': ('output_index', ReturnType.Single, self.parse_next_one),
            '[cash]': ('cash', ReturnType.Single, self.parse_next_one),
            '[creature minimum level]': (
                'creature_min_level',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature skill consume mp rate]': (
                'creature_skill_consume_mp_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature skill over charge time rate]': (
                'creature_skill_over_charge_time_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature experience amount rate]': (
                'creature_experience_amount_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature physical critical hit]': (
                'creature_physical_critical_hit',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature magical critical hit]': (
                'creature_magical_critical_hit',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[creature stuck]': (
                'creature_stuck',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[emancipate]': ('emancipate', ReturnType.Single, self.parse_emancipate),
            '[input]': ('input', ReturnType.Single, self.parse_until_close_segment),
            '[output]': ('output', ReturnType.Single, self.parse_until_close_segment),
            '[emancipate explain]': (
                'emancipate_explain',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[minimum rank]': ('minimum_rank', ReturnType.Single, self.parse_next_one),
            '[usable world]': (
                'usable_world',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[expertjob only]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/expertjob only]'),
            ),
            '[prof compound rate]': (
                'prof_compound_rate',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[prof additional gain exp]': (
                'prof_additional_gain_exp',
                ReturnType.Single,
                self.parse_until_segment,
            ),
            '[prof result variation]': (
                'prof_result_variation',
                ReturnType.Single,
                self.parse_until_segment,
            ),
            '[prof disjoint result variation]': (
                'prof_disjoint_result_variation',
                ReturnType.Single,
                self.parse_until_segment,
            ),
            '[prof material variation]': (
                'prof_material_variation',
                ReturnType.Single,
                self.parse_until_segment,
            ),
            '[rigidity]': ('rigidity', ReturnType.Single, self.parse_next_one),
            '[lift up]': ('lift_up', ReturnType.Single, self.parse_next_one),
            '[aurora avatar]': (
                'aurora_avatar',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[aura ability]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/aura ability]'),
            ),
            '[aurora graphic effects]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/aurora graphic_effects]'),
            ),
            '[hide equipment]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/hide equipment]'),
            ),
            '[hide layer]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/hide layer]'),
            ),
            '[clear avatar]': ('clear_avatar', ReturnType.Single, self.parse_next_one),
            '[special monster drop]': (
                'special_monster_drop',
                ReturnType.Single,
                self.parse_next_one,
            ),
            '[difficulty for extra drop]': (
                'difficulty_for_extra_drop',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[dungeon type for extra drop]': (
                'dungeon_type_for_extra_drop',
                ReturnType.Single,
                self.parse_until_close_segment,
            ),
            '[recovery status]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/recovery status]'),
            ),
            '[character item check]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/character item check]'),
            ),
            '[hardcoding parameter]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/hardcoding parameter]'),
            ),
            '[command]': ('-', ReturnType.NoneValue, self.skip_until('[/command]')),
            '[expiration date]': ('-', ReturnType.NoneValue, self.parse_until_segment),
            '[level section ani]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/level section ani]'),
            ),
            '[level section ability]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/level section ability]'),
            ),
            '[limit upgradable level]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/limit upgradable level]'),
            ),
            '[variable stat]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/variable stat]'),
            ),
            '[expand ani]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/expand ani]'),
            ),
            '[emblem socket default]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/emblem socket default]'),
            ),
            '[particle]': ('-', ReturnType.NoneValue, self.skip_until('[/particle]')),
            '[effect]': ('-', ReturnType.NoneValue, self.skip_until('[/effect]')),
            '[hide grow avatar]': (
                '-',
                ReturnType.NoneValue,
                self.skip_until('[/hide grow avatar]'),
            ),
        }

    def parse_piece_set(self) -> PieceSet:
        res = PieceSet()
        while self.idx < self.total:
            it = self.current_item()
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_piece_set_ability(self) -> PieceSetAbility:
        self.idx += 1
        res = PieceSetAbility()
        res.part_count = self.current_item()[1]
        self.idx += 1
        while self.idx < self.total:
            it = self.current_item()
            if it[1] == '[/piece set ability]':  # end of segment
                break
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_skill_level_up(self) -> List[SkillLevelUp]:
        res: List[SkillLevelUp] = []
        while self.bc[self.idx + 1][1] != '[/skill levelup]':
            res.append(
                SkillLevelUp(
                    role=self.bc[self.idx + 1][1],
                    skill_id=self.bc[self.idx + 2][1],
                    level_up=self.bc[self.idx + 3][1],
                )
            )
            self.idx += 3
        self.idx += 1
        return res

    def parse_item_aura(self) -> ItemAura:
        res = ItemAura(
            aura_type=self.next_n_item(1)[1],
            op=self.next_n_item(2)[1],
            num=self.next_n_item(3)[1],
            distance=self.next_n_item(4)[1],
        )
        self.idx += 4
        return res

    def parse_quest(self) -> Quest:
        res = Quest()
        while self.idx < self.total:
            it = self.current_item()
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_equipment(self) -> Equipment:
        res = Equipment()
        while self.idx < self.total:
            it = self.current_item()
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_set_ability(self) -> SetAbility:
        self.idx += 1
        res = SetAbility()
        while self.idx < self.total:
            it = self.current_item()
            if it[1] == '[/set ability]':  # end of segment
                break
            if (
                it[0] == 5 and it[1] == '[set name]'
            ):  # this segment is duplicated in global space
                res.set_name = self.next_n_item(1)[1]
                self.idx += 2
                continue
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_avatar_select_ability(self) -> List[AvatarSelectAbility]:
        res: List[AvatarSelectAbility] = []
        while (
            self.idx < self.total - 1
            and self.next_n_item(1)[1] != '[/avatar select ability]'
        ):
            # todo implement it later skip by now
            self.idx += 1
        self.idx += 1
        return res

    def parse_all_skill_item(self):
        self.idx += 1
        res = AllSkillItem()
        while self.idx < self.total:
            it = self.current_item()
            if it[1] == '[/all skill item]':  # end of segment
                break
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_skill_apply_condition(self):
        self.idx += 1
        res = SkillApplyCondition()
        while self.idx < self.total:
            it = self.current_item()
            if it[1] == '[/skill apply condition]':  # end of segment
                break
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_emancipate(self):
        self.idx += 1
        res = Emancipate()
        while self.idx < self.total:
            it = self.current_item()
            if it[1] == '[/emancipate]':  # end of segment
                break
            if it[0] == 5:
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_properties(self, obj: object, segment_key: str):
        attr, rtt, pf = self.get_parse_function(segment_key)
        v = pf()
        if rtt == ReturnType.NoneValue:
            return
        elif rtt == ReturnType.Single:
            try:
                setattr(obj, attr, v)
            except Exception as e:
                print(e)
        elif rtt == ReturnType.List:
            vv = getattr(obj, attr, [])
            vv.append(v)
            setattr(obj, attr, vv)

    def parse_next_one(self) -> object:
        self.idx += 1
        return self.current_item()[1]

    def parse_next_n(self, n: int) -> parse_function_type:
        def parse_next_n() -> object:
            res = []
            for _ in range(n):
                self.idx += 1
                res.append(self.current_item()[1])
            return res

        return parse_next_n

    def parse_until_segment(self) -> object:
        res = []
        while self.idx < self.total - 1 and self.next_n_item(1)[0] != 5:
            self.idx += 1
            res.append(self.current_item()[1])
        return res

    def parse_until_close_segment(self) -> object:
        res = self.parse_until_segment()
        self.idx += 1
        return res

    def skip_next_n(self, n: int) -> parse_function_type:
        def skip_next_inner():
            self.idx = min(self.total - 1, self.idx + n)
            return None

        return skip_next_inner

    def skip_until(self, close_tag: str) -> parse_function_type:
        def skip_until_inner() -> object:
            try:
                while self.idx < self.total and self.current_item()[1] != close_tag:
                    self.idx += 1
            except IndexError as e:
                print(e)
            return None

        return skip_until_inner

    def skip_until_segment(self):
        while self.idx < self.total - 1 and self.next_n_item(1)[0] != 5:
            self.idx += 1

    def get_parse_function(self, segment: str):
        attr, rtt, pf = self.parse_function_map.get(segment, (None, None, None))
        # ignore all not defined segments
        if attr is None or pf is None:
            attr = '-'
            rtt = ReturnType.NoneValue
            pf = self.skip_until_segment
        return attr, rtt, pf

    def current_item(self) -> BinaryItem:
        return self.bc[self.idx]

    def next_n_item(self, n: int) -> BinaryItem:
        return self.bc[self.idx + n]
