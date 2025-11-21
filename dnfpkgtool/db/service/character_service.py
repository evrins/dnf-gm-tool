from enum import Enum

from config import config
from dnfpkgtool.db.entity.account_money import AccountMoney
from dnfpkgtool.db.entity.character_points import CharacterPoints
from dnfpkgtool.db.model.cash_cera import CashCera
from dnfpkgtool.db.model.cash_cera_point import CashCeraPoint
from dnfpkgtool.db.model.character_blood_dungeon_reward import (
    CharacterBloodDungeonReward,
)
from dnfpkgtool.db.model.character_dimension_inout import CharacterDimensionInout
from dnfpkgtool.db.model.character_info import CharacterInfo
from dnfpkgtool.db.model.character_manage_info import CharacterManageInfo
from dnfpkgtool.db.model.character_quest_shop import CharacterQuestShop
from dnfpkgtool.db.model.character_stat import CharacterStat
from dnfpkgtool.db.model.limit_create_character import LimitCreateCharacter
from dnfpkgtool.db.model.member_dungeon import MemberDungeon
from dnfpkgtool.db.model.pvp_result import PVPResult
from dnfpkgtool.db.model.skill import Skill
from dnfpkgtool.db.repo.account_cargo_repo import get_account_cargo_repo
from dnfpkgtool.db.repo.cash_cera_point_repo import get_cash_cera_point_repo
from dnfpkgtool.db.repo.cash_cera_repo import get_cash_cera_repo
from dnfpkgtool.db.repo.character_blood_dungeon_reward_repo import (
    get_character_blood_dungeon_reward_repo,
)
from dnfpkgtool.db.repo.character_dimension_inout_repo import (
    get_character_dimension_inout_repo,
)
from dnfpkgtool.db.repo.character_info_repo import get_character_info_repo
from dnfpkgtool.db.repo.character_manage_info_repo import get_character_manage_info_repo
from dnfpkgtool.db.repo.character_quest_shop_repo import get_character_quest_shop_repo
from dnfpkgtool.db.repo.character_stat_repo import get_character_stat_repo
from dnfpkgtool.db.repo.inventory_repo import get_inventory_repo
from dnfpkgtool.db.repo.limit_create_character_repo import (
    get_limit_create_character_repo,
)
from dnfpkgtool.db.repo.member_dungeon_repo import get_member_dungeon_repo
from dnfpkgtool.db.repo.member_punish_info_repo import get_member_punish_info_repo
from dnfpkgtool.db.repo.pvp_result_repo import get_pvp_result_repo
from dnfpkgtool.db.repo.skill_repo import get_skill_repo
from dnfpkgtool.repo.repo_manager import get_dungeon_repo, get_exp_repo


class ChargeType(Enum):
    CashCera = 1
    CashCeraPoint = 2
    SP = 3
    QP = 4
    TP = 5


class CharacterService:
    def __init__(self):
        self.pvp_result_repo = get_pvp_result_repo()
        self.account_cargo_repo = get_account_cargo_repo()
        self.inventory_repo = get_inventory_repo()
        self.character_info_repo = get_character_info_repo()
        self.character_stat_repo = get_character_stat_repo()
        self.character_quest_shop_repo = get_character_quest_shop_repo()
        self.cash_cera_repo = get_cash_cera_repo()
        self.cash_cera_point_repo = get_cash_cera_point_repo()
        self.skill_repo = get_skill_repo()
        self.limit_create_character_repo = get_limit_create_character_repo()
        self.character_blood_dungeon_reward_repo = (
            get_character_blood_dungeon_reward_repo()
        )
        self.character_dimension_inout_repo = get_character_dimension_inout_repo()
        self.character_manage_info_repo = get_character_manage_info_repo()
        self.member_dungeon_repo = get_member_dungeon_repo()
        self.member_punish_info_repo = get_member_punish_info_repo()

        self.exp_repo = get_exp_repo()
        self.dungeon_repo = get_dungeon_repo()

    def get_current_character_pvp_result(self) -> PVPResult:
        character_no = config.get_current_character_no()
        res = self.pvp_result_repo.query_by_character_no(character_no)
        if not res:
            res = PVPResult(
                character_no=character_no, pvp_grade=0, win_point=0, pvp_point=0, win=0
            )
        return res

    def update_current_character_pvp_result(self, pvp_result: PVPResult):
        character_no = config.get_current_character_no()
        pvp_result.character_no = character_no
        self.pvp_result_repo.update(pvp_result)

    def get_current_character_info(self) -> CharacterInfo:
        character_no = config.get_current_character_no()
        res = self.character_info_repo.query_by_character_no(character_no)
        return res

    def update_current_character_info(
            self, character_info: CharacterInfo, has_level_changed: bool
    ):
        m_id = config.get_current_account_id()
        character_no = config.get_current_character_no()
        character_info.character_no = character_no
        if has_level_changed:
            exp = self.exp_repo.query_by_level(character_info.lev) + 1
            self.character_stat_repo.update_exp(
                CharacterStat(character_no=character_no, exp=exp)
            )
            self.member_punish_info_repo.delete_by_m_id(m_id)
        self.character_info_repo.update_character_info(character_info)

    def get_current_account_money(self):
        res = AccountMoney()
        mid = config.get_current_account_id()
        res.account_cargo_money = self.account_cargo_repo.query_money_by_m_id(mid)
        if not res.account_cargo_money:
            res.account_cargo_money = 0

        character_no = config.get_current_character_no()
        res.backpack_money = self.inventory_repo.query_money_by_character_no(
            character_no
        )
        res.pay_coin = self.inventory_repo.query_pay_coin_by_character_no(character_no)

        return res

    def update_current_account_money(self, account_money: AccountMoney):
        mid = config.get_current_account_id()
        self.account_cargo_repo.update_money_by_m_id(
            mid, account_money.account_cargo_money
        )

        character_no = config.get_current_character_no()
        self.inventory_repo.update_money_by_character_no(
            character_no, account_money.backpack_money
        )
        self.inventory_repo.update_pay_coin_by_character_no(
            character_no, account_money.pay_coin
        )

    def get_current_character_points(self) -> CharacterPoints:
        res = CharacterPoints()
        mid = config.get_current_account_id()

        account_id = f'{mid}'
        res.cash_cera = self.cash_cera_repo.query_cera_by_account(account_id)
        res.cash_cera_point = self.cash_cera_point_repo.query_cera_point_by_account(
            account_id
        )
        character_no = config.get_current_character_no()
        skill = self.skill_repo.query_by_character_no(character_no)
        res.skill_point = skill.remain_sp
        res.tp = skill.remain_sfp_1st
        res.quest_point = self.character_quest_shop_repo.query_qp_by_character_no(
            character_no
        )

        return res

    def charge_points(self, charge_type: ChargeType, num: int):
        mid = config.get_current_account_id()
        account_id = f'{mid}'
        character_no = config.get_current_character_no()
        if charge_type == ChargeType.CashCera:
            self.cash_cera_repo.charge_cera(CashCera(account=account_id, cera=num))
        elif charge_type == ChargeType.CashCeraPoint:
            self.cash_cera_point_repo.charge_cera_point(
                CashCeraPoint(account=account_id, cera_point=num)
            )
        elif charge_type == ChargeType.SP:
            self.skill_repo.charge(
                Skill(charac_no=character_no, remain_sp=num, remain_sp_2nd=num)
            )
        elif charge_type == ChargeType.TP:
            self.skill_repo.charge(
                Skill(charac_no=character_no, remain_sfp_1st=num, remain_sfp_2nd=num)
            )
        elif charge_type == ChargeType.QP:
            self.character_quest_shop_repo.charge(
                CharacterQuestShop(charac_no=character_no, qp=num)
            )

    def clear_points(self, charge_type: ChargeType):
        mid = config.get_current_account_id()
        account_id = f'{mid}'
        character_no = config.get_current_character_no()
        if charge_type == ChargeType.CashCera:
            self.cash_cera_repo.clear_cera_by_account(account_id)
        elif charge_type == ChargeType.CashCeraPoint:
            self.cash_cera_point_repo.clear_cera_point_by_account(account_id)
        elif charge_type == ChargeType.SP:
            self.skill_repo.clear_sp_by_character_no(character_no)
        elif charge_type == ChargeType.TP:
            self.skill_repo.clear_tp_by_character_no(character_no)
        elif charge_type == ChargeType.QP:
            self.character_quest_shop_repo.clear_qp_by_character_no(character_no)

    def enable_current_character_left_and_right_slot(self):
        character_no = config.get_current_character_no()
        self.character_stat_repo.update_add_slot_flag(
            CharacterStat(character_no=character_no, add_slot_flag=3)
        )

    def remove_current_account_add_character_limit(self):
        m_id = config.get_current_account_id()
        self.limit_create_character_repo.update(
            LimitCreateCharacter(m_id=m_id, count=0)
        )
        self.member_punish_info_repo.delete_by_m_id(m_id)

    def reset_current_character_dungeon_count(self):
        character_no = config.get_current_character_no()
        self.character_blood_dungeon_reward_repo.update(
            CharacterBloodDungeonReward(character_no=character_no, enter_count=0)
        )
        self.character_dimension_inout_repo.update(
            CharacterDimensionInout(
                character_no=character_no,
                dungeon1=6,
                dungeon2=6,
                dungeon3=6,
                dungeon4=6,
                dungeon5=6,
                dungeon6=6,
                dungeon7=6,
                dungeon8=6,
                dungeon9=6,
                dungeon10=6,
            )
        )

    def remove_current_character_equipment_level_limit(self):
        character_no = config.get_current_character_no()
        self.character_manage_info_repo.upsert(
            CharacterManageInfo(character_no=character_no, max_equip_level=999)
        )

    def enable_current_account_all_dungeon_difficulty(self):
        mid = config.get_current_account_id()
        self.member_dungeon_repo.update(
            MemberDungeon(m_id=mid, dungeon=self.dungeon_repo.dungeon_unlock())
        )

    def max_current_character_expert_job_level(self):
        character_no = config.get_current_character_no()
        self.character_stat_repo.update_expert_level(
            CharacterStat(character_no=character_no, expert_job_exp=2054)
        )


def get_character_service() -> CharacterService:
    return CharacterService()
