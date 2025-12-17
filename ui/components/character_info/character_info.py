from config import config
from dnf_db.entity.account_money import AccountMoney
from dnf_db.entity.signals import gs
from dnf_db.model.character_info import CharacterInfo
from dnf_db.model.pvp_result import PVPResult
from dnf_db.service.account_service import expert_jobs, jobs
from dnf_db.service.character_service import ChargeType, get_character_service
from PySide6.QtWidgets import QWidget

from ui.components.character_info.character_info_ui import Ui_character_info

roles = [
    '鬼剑士',
    '格斗家',
    '神枪手',
    '魔法师',
    '圣职者',
    '神枪手-女',
    '暗夜使者',
    '格斗家-男',
    '魔法师-男',
    '黑暗武士',
    '缔造者',
]

pvp_grades = [
    '10级',
    '9级',
    '8级',
    '7级',
    '6级',
    '5级',
    '4级',
    '3级',
    '2级',
    '1级',
    '1段',
    '2段',
    '3段',
    '4段',
    '5段',
    '6段',
    '7段',
    '8段',
    '9段',
    '10段',
    '至尊1',
    '至尊2',
    '至尊3',
    '至尊4',
    '至尊5',
    '至尊6',
    '至尊7',
    '至尊8',
    '至尊9',
    '至尊10',
    '达人',
    '名人',
    '小霸王',
    '霸王',
    '斗神',
]


class CharacterInfoWidget(QWidget, Ui_character_info):
    character_level = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.character_service = get_character_service()

        self.role_combox.addItems(roles)
        self.role_combox.currentIndexChanged.connect(self.update_job_options)
        self.expert_combox.addItems(expert_jobs)
        self.wake_combox.addItems(['无', '一觉', '二觉'])
        self.save_character_info_btn.clicked.connect(self.save_character_info)

        self.grade_combox.addItems(pvp_grades)
        self.save_pvp_btn.clicked.connect(self.save_pvp)

        self.save_coin_btn.clicked.connect(self.save_account_money)

        self.charge_type_combox.addItems(['点券', '代币', 'SP', 'QP', 'TP'])
        self.charge_btn.clicked.connect(self.charge_points)
        self.clear_btn.clicked.connect(self.clear_points)

        self.remove_add_character_limit_btn.clicked.connect(
            self.remove_add_character_limit
        )
        self.reset_dungeon_count_btn.clicked.connect(self.reset_dungeon_count)
        self.remove_equipment_level_limit_btn.clicked.connect(
            self.remove_equipment_level_limit
        )
        self.enable_all_dungeon_difficulty_btn.clicked.connect(
            self.enable_all_dungeon_difficulty
        )
        self.enable_left_and_right_slot_btn.clicked.connect(
            self.enable_left_and_right_slot
        )
        self.max_expert_job_level_btn.clicked.connect(self.max_expert_job_level)
        self.reset_fatigue_btn.clicked.connect(self.reset_fatigue)

        self.refresh_btn.clicked.connect(self.refresh)

        gs.character_no_changed.connect(self.refresh)

        self.refresh()

    def refresh(self):
        if not config.have_valid_account_id_and_character_no():
            return
        self.init_pvp()
        self.init_character_info()
        self.init_account_money()
        self.init_points()

    def init_pvp(self):
        pvp_result = self.character_service.get_current_character_pvp_result()
        self.grade_combox.setCurrentIndex(pvp_result.pvp_grade)
        self.win_spinbox.setValue(pvp_result.win)
        self.win_point_spin_box.setValue(pvp_result.win_point)

    def save_pvp(self):
        pvp_result = PVPResult()
        pvp_result.pvp_grade = self.grade_combox.currentIndex()
        pvp_result.win = self.win_spinbox.value()
        pvp_result.win_point = self.win_point_spin_box.value()
        pvp_result.pvp_point = pvp_result.win_point
        self.character_service.update_current_character_pvp_result(pvp_result)

    def init_character_info(self):
        character_info = self.character_service.get_current_character_info()
        self.name_line_edit.setText(character_info.character_name)
        self.character_level = character_info.lev
        self.level_spin_box.setValue(self.character_level)
        self.role_combox.setCurrentIndex(character_info.job)
        grow_type = character_info.grow_type % 16
        wake_flag = character_info.grow_type // 16

        self.job_combox.setCurrentIndex(grow_type)
        self.wake_combox.setCurrentIndex(wake_flag)
        self.expert_combox.setCurrentIndex(character_info.expert_job)

    def save_character_info(self):
        grow_type = (
            self.job_combox.currentIndex() + self.wake_combox.currentIndex() * 16
        )

        character_info = CharacterInfo(
            lev=self.level_spin_box.value(),
            job=self.role_combox.currentIndex(),
            grow_type=grow_type,
            expert_job=self.expert_combox.currentIndex(),
        )

        has_level_changed = character_info.lev != self.character_level
        self.character_service.update_current_character_info(
            character_info, has_level_changed
        )

        gs.character_info_changed.emit()

    def update_job_options(self):
        self.job_combox.clear()
        self.job_combox.addItems(jobs[self.role_combox.currentIndex()])

    def init_account_money(self):
        account_money = self.character_service.get_current_account_money()
        self.cargo_coin_spin_box.setValue(account_money.account_cargo_money)
        self.backpack_coin_spin_box.setValue(account_money.backpack_money)
        self.pay_coin_spin_box.setValue(account_money.pay_coin)

    def save_account_money(self):
        account_money = AccountMoney(
            account_cargo_money=self.cargo_coin_spin_box.value(),
            backpack_money=self.backpack_coin_spin_box.value(),
            pay_coin=self.pay_coin_spin_box.value(),
        )
        self.character_service.update_current_account_money(account_money)

    def init_points(self):
        cp = self.character_service.get_current_character_points()
        self.cash_cera_spin_box.setValue(cp.cash_cera)
        self.cash_cera_point_spin_box.setValue(cp.cash_cera_point)
        self.sp_spin_box.setValue(cp.skill_point)
        self.qp_spin_box.setValue(cp.quest_point)
        self.tp_spin_box.setValue(cp.tp)

    def charge_points(self):
        num = self.charge_spin_box.value()
        num = int(num)
        if num == 0:
            return
        charge_type = self.charge_type_combox.currentText()
        charge_type = to_charge_type(charge_type)
        self.character_service.charge_points(charge_type, num)
        self.init_points()

    def clear_points(self):
        charge_type = self.charge_type_combox.currentText()
        charge_type = to_charge_type(charge_type)
        self.character_service.clear_points(charge_type)
        self.init_points()

    def remove_add_character_limit(self):
        self.character_service.remove_current_account_add_character_limit()

    def reset_dungeon_count(self):
        self.character_service.reset_current_character_dungeon_count()

    def enable_left_and_right_slot(self):
        self.character_service.enable_current_character_left_and_right_slot()

    def remove_equipment_level_limit(self):
        self.character_service.remove_current_character_equipment_level_limit()

    def enable_all_dungeon_difficulty(self):
        self.character_service.enable_current_account_all_dungeon_difficulty()

    def max_expert_job_level(self):
        self.character_service.max_current_character_expert_job_level()

    def reset_fatigue(self):
        self.character_service.reset_current_character_fatigue()


def to_charge_type(text: str) -> ChargeType:
    if text == '点券':
        charge_type = ChargeType.CashCera
    elif text == '代币':
        charge_type = ChargeType.CashCeraPoint
    elif text == 'SP':
        charge_type = ChargeType.SP
    elif text == 'QP':
        charge_type = ChargeType.QP
    elif text == 'TP':
        charge_type = ChargeType.TP
    else:
        raise ValueError('Charge type not supported')
    return charge_type
