from PySide6.QtWidgets import QWidget

from dnfpkgtool.db.entity.mail_form_item import MailFormItem
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from ui.components.mail.stackable_form_ui import Ui_stackable_form


class StackableForm(QWidget, Ui_stackable_form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.item_id = 0
        self.item_type = None

    def set_item(self, mail_item: MailSubmitItem):
        self.id_line_edit.setText(str(mail_item.item_id))
        self.name_line_edit.setText(mail_item.item_name)
        self.num_spin_box.setValue(0)
        self.gold_spin_box.setValue(0)

        self.item_id = mail_item.item_id
        self.item_type = mail_item.item_type

    def get_item(self) -> MailFormItem:
        return MailFormItem(
            item_id=self.item_id,
            item_type=self.item_type,
            num=self.num_spin_box.value(),
            gold=self.gold_spin_box.value(),
        )
