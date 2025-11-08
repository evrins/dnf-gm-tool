from PySide6.QtWidgets import QWidget

from config import config
from dnfpkgtool.db.entity.dnf_item_slot import reinforce_type_dict
from dnfpkgtool.db.entity.mail_form_item import MailFormItem, MailItemType
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from ui.components.mail.equipment_form_ui import Ui_equipment_form


class EquipmentForm(QWidget, Ui_equipment_form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.item_id = 0
        self.item_type = None
        self.sub_type = 0

        self.max_btn.clicked.connect(self.set_max_grade)
        self.reinforce_type_combox.addItems(list(reinforce_type_dict.values()))

    def set_item(self, mail_item: MailSubmitItem):
        self.id_line_edit.setText(str(mail_item.item_id))
        self.name_line_edit.setText(mail_item.item_name)
        if mail_item.item_type == MailItemType.Equipment:
            self.grade_spin_box.setValue(config.MAX_GRADE)  # 最上级 99%
        else:
            self.grade_spin_box.setValue(0)
        self.endurance_spin_box.setValue(mail_item.endurance)

        self.item_id = mail_item.item_id
        self.item_type = mail_item.item_type
        self.sub_type = mail_item.sub_type

    def get_item(self) -> MailFormItem:
        return MailFormItem(
            item_id=self.item_id,
            item_type=self.item_type,
            gold=self.gold_spin_box.value(),
            num=1,
            grade=self.grade_spin_box.value(),
            amplify_option=self.reinforce_type_combox.currentIndex(),
            amplify_value=self.reinforce_value_spin_box.value(),
            upgrade=self.enhance_level_spin_box.value(),
            separate_upgrade=self.forge_level_spin_box.value(),
            seal_flag=1 if self.seal_checkbox.isChecked() else 0,
            endurance=self.endurance_spin_box.value(),
            sub_type=self.sub_type,
        )

    def set_max_grade(self):
        self.grade_spin_box.setValue(config.MAX_GRADE)
