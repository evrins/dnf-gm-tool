from PySide6.QtWidgets import QWidget

from dnf_db.entity.mail_form_item import MailFormItem
from dnf_db.entity import MailSubmitItem
from ui.components.mail.stackable_form_ui import Ui_stackable_form


class StackableForm(QWidget, Ui_stackable_form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.item_id = 0
        self.item_type = None
        self.stack_limit = 1

        self.max_btn.clicked.connect(self.set_item_stack_limit)

    def set_item(self, mail_item: MailSubmitItem):
        self.stack_limit = mail_item.stack_limit if mail_item.stack_limit > 1 else 1

        self.id_line_edit.setText(str(mail_item.item_id))
        self.name_line_edit.setText(mail_item.item_name)
        self.num_spin_box.setValue(self.stack_limit)
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

    def set_item_stack_limit(self):
        self.num_spin_box.setValue(self.stack_limit)
