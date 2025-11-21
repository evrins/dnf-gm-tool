from enum import Enum
from typing import Callable, List

from dnfpkgtool.pvf.entity.binary_content import BinaryContent, BinaryItem
from dnfpkgtool.pvf.entity.item_aura import ItemAura
from dnfpkgtool.pvf.entity.piece_set import PieceSet
from dnfpkgtool.pvf.entity.piece_set_ability import PieceSetAbility
from dnfpkgtool.pvf.entity.quest import Quest
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
            '[active status control info]': (
                'active_status_control_info',
                ReturnType.NoneValue,
                self.skip_next_n(5),
            ),
            '[if]': ('if', ReturnType.NoneValue, self.skip_until('[/if]')),
            '[then]': ('then', ReturnType.NoneValue, self.skip_until('[/then]')),
            '[skill data up]': (
                'skill_data_up',
                ReturnType.NoneValue,
                self.skip_until('[/skill data up]'),
            ),
            '[multiple then]': (
                'multiple then',
                ReturnType.NoneValue,
                self.skip_until('[/multiple then]'),
            ),
            '[all skill item container]': (
                'all_skill_item_container',
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
            '[effect after clear quest]': (
                'effect_after_clear_quest',
                ReturnType.NoneValue,
                self.skip_next_n(1),
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
            '[appear map]': ('appear_map', ReturnType.NoneValue, self.skip_next_n(4)),
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
            '[ignore quest level 4 exp]': (
                'ignore_quest_level_4_exp',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[exception quest]': (
                'exception_quest',
                ReturnType.NoneValue,
                self.parse_until_close_segment,
            ),
            '[exposed by npc]': (
                'exposed_by_npc',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[job message]': ('job_message', ReturnType.NoneValue, self.skip_next_n(1)),
            '[go guide]': ('go_guide', ReturnType.NoneValue, self.skip_next_n(5)),
            '[cant giveup]': (
                'cant_give_up',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[show click on complete npc]': (
                'show_click_on_complete_npc',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[job change quest]': (
                'job_change_quest',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[clear reward item]': (
                'clear_reward_item',
                ReturnType.NoneValue,
                self.skip_until('[/clear reward item]'),
            ),
            '[grow number]': ('grow_number', ReturnType.NoneValue, self.skip_next_n(1)),
            '[delete npc index]': (
                'delete_npc_index',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[creature kind]': (
                'creature_kind',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[creature level]': (
                'creature_level',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[collision quest]': (
                'collision_quest',
                ReturnType.NoneValue,
                self.skip_until('[/collision quest]'),
            ),
            '[mail time]': ('mail_time', ReturnType.NoneValue, self.skip_next_n(1)),
            '[mail title]': ('mail_title', ReturnType.NoneValue, self.skip_next_n(1)),
            '[mail contents]': (
                'mail_contents',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[event]': ('event', ReturnType.NoneValue, self.skip_next_n(1)),
            '[searching information]': (
                'searching_information',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[hide npc on clear]': (
                'hide_npc_on_clear',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[first exposed by npc]': (
                'first_exposed_by_npc',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[expertjob level]': (
                'expertjob_level',
                ReturnType.NoneValue,
                self.skip_next_n(2),
            ),
            '[limit dungeon index]': (
                'collision_quest',
                ReturnType.NoneValue,
                self.skip_until('[/limit dungeon index]'),
            ),
            '[check count]': (
                'check_count',
                ReturnType.NoneValue,
                self.skip_until('[/check count]'),
            ),
            '[limit showing msg]': (
                'limit_showing_msg',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[condition data]': (
                'condition_data',
                ReturnType.NoneValue,
                self.skip_until('[/condition data]'),
            ),
            '[send postal]': ('send_postal', ReturnType.NoneValue, self.skip_next_n(4)),
            '[string data]': (
                'string_data',
                ReturnType.NoneValue,
                self.skip_until('[/string data]'),
            ),
            '[show npc on clear]': (
                'show_npc_on_clear',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[quest piece]': ('-', ReturnType.NoneValue, self.skip_next_n(1)),
            '[isNotClear LevelUp System]': (
                '-',
                ReturnType.NoneValue,
                self.skip_next_n(1),
            ),
            '[schedule]': ('-', ReturnType.NoneValue, self.skip_until('[/schedule]')),
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
                if it[1] == '[level]':
                    pass
                self.parse_properties(res, it[1])
            self.idx += 1
        return res

    def parse_properties(self, obj: object, segment_key: str):
        attr, rtt, pf = self.get_parse_function(segment_key)
        v = pf()
        if rtt == ReturnType.NoneValue:
            return
        elif rtt == ReturnType.Single:
            setattr(obj, attr, v)
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
        while self.next_n_item(1)[0] != 5:
            self.idx += 1
            res.append(self.current_item()[1])
        return res

    def parse_until_close_segment(self) -> object:
        res = self.parse_until_segment()
        self.idx += 1
        return res

    def skip_next_n(self, n: int) -> parse_function_type:
        def skip_next_inner():
            self.idx += n
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

    def get_parse_function(self, segment: str):
        attr, rtt, pf = self.parse_function_map.get(segment, (None, None, None))
        if attr is None or pf is None:
            attr = segment.replace('[', '').replace(']', '').replace(' ', '_').lower()
            rtt = ReturnType.Single
            pf = self.parse_next_one
        return attr, rtt, pf

    def current_item(self) -> BinaryItem:
        return self.bc[self.idx]

    def next_n_item(self, n: int) -> BinaryItem:
        return self.bc[self.idx + n]
