from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot
from ui.components.inventory.inventory_stackable_form_ui import (
    Ui_inventory_stackable_form,
)


class StackableForm(QWidget, Ui_inventory_stackable_form):
    on_save = Signal(DnfItemSlot)
    on_delete = Signal(DnfItemSlot)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.origin_item: DnfItemSlot = DnfItemSlot.default()

        self.save_btn.clicked.connect(self.save)
        self.reset_btn.clicked.connect(self.reset)
        self.delete_btn.clicked.connect(self.delete)

    def set_item(self, item: DnfItemSlot):
        self.origin_item = item

        self._set_item(item)

    def _set_item(self, item: DnfItemSlot):
        self.id_line_edit.setText(str(item.id))
        self.name_line_edit.setText(item.display_name)
        if item.stack_limit <= 0:
            self.num_spin_box.setMaximum(999999999)
        else:
            self.num_spin_box.setMaximum(item.stack_limit)
        self.num_spin_box.setValue(item.num_grade)

    def save(self):
        new_item: DnfItemSlot = self.origin_item.model_copy(deep=True)
        new_item.num_grade = self.num_spin_box.value()

        self.on_save.emit(new_item)

    def reset(self):
        self._set_item(self.origin_item)

    def delete(self):
        self.on_delete.emit(self.origin_item)
