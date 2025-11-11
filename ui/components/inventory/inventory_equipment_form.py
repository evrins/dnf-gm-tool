from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget

from config import config
from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot, reinforce_type_dict
from dnfpkgtool.db.entity.magic_seal import MagicSeal
from dnfpkgtool.repo.magic_seal_repo import get_magic_seal_repo
from dnfpkgtool.repo.orb_repo import get_orb_repo
from ui.components.inventory.inventory_equipment_form_ui import (
    Ui_inventory_equipment_form,
)

orb_part_options = {
    '[magic stone]': ['物理攻击力', '魔法攻击力', '独立攻击力', '所有属性强化'],
    '[pants]': [
        '火属性抗性',
        '暗属性抗性',
        '所有属性抗性',
        '物理暴击率',
        '魔法暴击率',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '攻击速度',
        '释放速度',
        '移动速度',
        '硬直',
        '特殊效果',
    ],
    '[shoes]': [
        '回避率',
        '魔法防御',
        '物理防御',
        '物理暴击率',
        '魔法暴击率',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '移动速度',
        'HP 最大值',
        'MP 最大值',
        '跳跃力',
        '技能等级提升',
    ],
    '[title name]': [
        '魔法防御',
        '物理防御',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '所有属性强化',
        'HP 最大值',
        'MP 最大值',
        '僵直',
        '技能等级提升',
        '硬直',
    ],
    '[coat]': [
        '物理暴击率',
        '魔法暴击率',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '攻击速度',
        '释放速度',
    ],
    '[weapon]': [
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '攻击速度',
        '释放速度',
        '属性攻击',
        '命中率',
    ],
    '[waist]': [
        '魔法防御',
        '物理防御',
        '物理暴击率',
        '魔法暴击率',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        'HP 最大值',
        'MP 最大值',
        '技能等级提升',
    ],
    '[wrist]': [
        '火属性抗性',
        '光属性抗性',
        '力量',
        '智力',
        '独立攻击力',
        '火属性强化',
        '冰属性强化',
        '光属性强化',
        '暗属性强化',
        '所有属性强化',
        'HP 回复速度',
        '僵直',
    ],
    '[amulet]': [
        '所有异常状态抗性',
        '石化抗性',
        '束缚抗性',
        '火属性抗性',
        '力量',
        '智力',
        '独立攻击力',
        '火属性强化',
        '冰属性强化',
        '光属性强化',
        '暗属性强化',
        '所有属性强化',
        '僵直',
        '技能等级提升',
    ],
    '[foil]': [
        '火属性抗性',
        '物理暴击率',
        '魔法暴击率',
        '力量',
        '智力',
        '攻击速度',
        '释放速度',
        '移动速度',
        'HP 最大值',
        'MP 最大值',
        '硬直',
    ],
    '[shoulder]': [
        '魔法防御',
        '物理防御',
        '物理暴击率',
        '魔法暴击率',
        '物理攻击力',
        '魔法攻击力',
        '力量',
        '智力',
        '独立攻击力',
        '释放速度',
        'HP 最大值',
        'MP 最大值',
        '技能等级提升',
    ],
    '[unlimited challenge]': [
        '火属性抗性',
        '物理暴击率',
        '魔法暴击率',
        '攻击速度',
        '释放速度',
        'HP 最大值',
        'MP 最大值',
        '硬直',
    ],
    '[ring]': [
        '中毒抗性',
        '减速抗性',
        '火属性抗性',
        '力量',
        '智力',
        '独立攻击力',
        '火属性强化',
        '冰属性强化',
        '光属性强化',
        '暗属性强化',
        '所有属性强化',
        'MP 回复速度',
        '僵直',
    ],
    '[support]': [
        '物理攻击力',
        '魔法攻击力',
        '独立攻击力',
        '释放速度',
        '技能等级提升',
        '特殊效果',
    ],
}


class EquipmentForm(QWidget, Ui_inventory_equipment_form):
    on_save = Signal(DnfItemSlot)
    on_delete = Signal(DnfItemSlot)

    def __init__(self, parent=None):
        super(EquipmentForm, self).__init__(parent)
        self.setupUi(self)

        self.origin_item: DnfItemSlot = DnfItemSlot(b'')
        self.orb_list = []
        self.orb = None

        self.magic_seal_repo = get_magic_seal_repo()
        self.all_magic_seal = self.magic_seal_repo.query_all()
        self.id_to_index = {
            it['id']: idx + 1 for idx, it in enumerate(self.all_magic_seal)
        }
        all_magic_items = ['---'] + [it['name'] for it in self.all_magic_seal]

        self.orb_repo = get_orb_repo()
        self.orb_category.currentIndexChanged.connect(self.update_orb_item_options)

        self.ms_controllers = [
            (self.ms_1_combox, self.ms_1_spin_box),
            (self.ms_2_combox, self.ms_2_spin_box),
            (self.ms_3_combox, self.ms_3_spin_box),
            (self.ms_4_combox, self.ms_4_spin_box),
        ]

        for it in self.ms_controllers:
            it[0].addItems(all_magic_items)

        self.reinforce_type_combox.addItems(list(reinforce_type_dict.values()))

        self.max_btn.clicked.connect(self.set_max_grade)

        self.reset_btn.clicked.connect(self.reset_form)
        self.save_btn.clicked.connect(self.save_form)
        self.delete_btn.clicked.connect(self.delete_item)

    def set_item(self, item: DnfItemSlot):
        self.origin_item = item
        self.update_field_values(self.origin_item)

    def update_field_values(self, item: DnfItemSlot):
        self.id_line_edit.setText(str(item.id))
        self.name_line_edit.setText(item.display_name)
        self.is_sealed_checkbox.setChecked(item.is_sealed != 0)
        self.seal_count_spin_box.setValue(item.seal_count)
        self.grade_spin_box.setValue(item.num_grade)
        self.endurance_spin_box.setMaximum(item.endurance_limit)
        self.endurance_spin_box.setValue(item.endurance)
        self.reinforce_type_combox.setCurrentIndex(item.reinforce_type)
        self.reinforce_value_spin_box.setValue(item.reinforce_value)
        self.enhance_level_spin_box.setValue(item.enhancement_level)
        self.forge_level_spin_box.setValue(item.forge_level)

        self.orb_category.clear()
        options = orb_part_options.get(item.equipment_type, None)
        if options is None:
            self.orb_category.setDisabled(True)
        else:
            self.orb_category.addItems(
                ['---'] + orb_part_options.get(item.equipment_type)
            )
            self.orb_category.setDisabled(False)

        # set orb
        if item.card_id > 0:
            self.orb = self.orb_repo.query_by_card_id(item.card_id)
            enchant_category = self.orb['display_enchant_category']
            if len(enchant_category) > 0:
                first_enchant_category = enchant_category[0]
                self.orb_category.setCurrentText(first_enchant_category)

            orb_idx = -1
            for i, it in enumerate(self.orb_list):
                if it['card_id'] == item.card_id:
                    orb_idx = i + 1
                    break
            if orb_idx != -1:
                QTimer.singleShot(0, lambda: self.orb_item.setCurrentIndex(orb_idx))
        else:
            self.orb_category.setCurrentIndex(0)

        for i in range(0, 4):
            self.ms_controllers[i][1].clear()
            ms = item.display_magic_seals[i]
            if ms.id != 0:
                self.ms_controllers[i][0].setCurrentIndex(self.id_to_index[ms.id])
                self.ms_controllers[i][1].setValue(ms.level)
            else:
                self.ms_controllers[i][0].setCurrentIndex(0)

    def update_orb_item_options(self, idx):
        self.orb_list = (
            self.orb_repo.query_by_display_enchant_category_and_equipment_type(
                self.orb_category.currentText(), self.origin_item.equipment_type
            )
        )

        # more detail
        orb_display_list = ['---'] + [
            f'{it["orb_name"]} {it["display_effect"]}' for it in self.orb_list
        ]

        self.orb_item.clear()
        self.orb_item.addItems(orb_display_list)

    def set_max_grade(self):
        self.grade_spin_box.setValue(config.MAX_GRADE)

    def reset_form(self):
        self.update_field_values(self.origin_item)

    def save_form(self):
        new_item = self.origin_item.model_copy(deep=True)
        new_item.is_sealed = 1 if self.is_sealed_checkbox.isChecked() else 0
        new_item.seal_count = self.seal_count_spin_box.value()
        new_item.num_grade = int(self.grade_spin_box.value())
        new_item.endurance = self.endurance_spin_box.value()
        new_item.reinforce_type = self.reinforce_type_combox.currentIndex()
        new_item.reinforce_value = self.reinforce_value_spin_box.value()
        new_item.enhancement_level = self.enhance_level_spin_box.value()
        new_item.forge_level = self.forge_level_spin_box.value()

        if self.orb_item.currentIndex() == 0:
            new_item.card_id = 0
        else:
            new_item.card_id = self.orb_list[self.orb_item.currentIndex() - 1][
                'card_id'
            ]

        for i in range(0, 4):
            ms = MagicSeal()
            idx = self.ms_controllers[i][0].currentIndex()
            if idx > 0:
                ms.id = self.all_magic_seal[idx - 1]['id']
                ms.level = self.ms_controllers[i][1].value()
            new_item.display_magic_seals[i] = ms

        self.on_save.emit(new_item)

    def delete_item(self):
        self.on_delete.emit(self.origin_item)
