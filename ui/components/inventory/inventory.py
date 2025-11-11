import os
import sys
from typing import List

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from PySide6.QtWidgets import QApplication, QWidget

from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot, type_dict
from dnfpkgtool.db.service.item_service import ItemService
from ui.components.inventory.empty import Empty
from ui.components.inventory.inventory_equipment_form import EquipmentForm
from ui.components.inventory.inventory_stackable_form import StackableForm
from ui.components.inventory.inventory_ui import Ui_inventory_container

type_text = list(type_dict.values()) + ['全部']
type_keys = list(type_dict.keys()) + [0xFF]


class InventoryTableModel(QAbstractTableModel):
    def __init__(self, data: List[DnfItemSlot]):
        super().__init__()
        self._data = data
        self._headers = [
            'display_idx',
            'display_name',
            'num_grade',
            'display_category',
            'display_rarity_name',
        ]
        self._headers_display = ['ID', '名称', '数量', '种类', '稀有度']

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            key = self._headers[index.column()]
            if key == 'num_grade':
                if row.is_equipment:
                    return 1
                else:
                    return row.num_grade
            return row.__dict__[key]
        elif role == Qt.ItemDataRole.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers_display[section]
        return None

    def flags(self, index) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class InventoryWidget(QWidget, Ui_inventory_container):
    on_refresh: Signal = Signal()
    on_save: Signal = Signal(DnfItemSlot)
    on_delete: Signal = Signal(DnfItemSlot)

    def __init__(self, item_list: List[DnfItemSlot]):
        super().__init__()

        self.item_list: List[DnfItemSlot] = []
        self.display_item_list: List[DnfItemSlot] = []

        self.setupUi(self)

        self.items_table_view.clicked.connect(self.on_row_clicked)

        self.show_blank_chkbox.setChecked(True)
        self.show_blank_chkbox.clicked.connect(self.toggle_empty)

        self.type_combox.addItems(type_text)
        self.type_combox.setCurrentIndex(len(type_text) - 1)
        self.type_combox.currentIndexChanged.connect(self.filter_type)

        self.refresh_btn.clicked.connect(self.refresh)

        self.set_data(item_list)

        self.empty = Empty()
        self.form_stack_widget.addWidget(self.empty)

        self.equipment_form = EquipmentForm()
        self.equipment_form.on_save.connect(self.save)
        self.equipment_form.on_delete.connect(self.delete)
        self.form_stack_widget.addWidget(self.equipment_form)

        self.stackable_form = StackableForm()
        self.stackable_form.on_save.connect(self.save)
        self.stackable_form.on_delete.connect(self.delete)
        self.form_stack_widget.addWidget(self.stackable_form)

        self.form_stack_widget.setCurrentIndex(0)

    def toggle_empty(self, checked: bool):
        self.update_table_view_item()

    def set_data(self, item_list: List[DnfItemSlot]):
        self.item_list = item_list
        self.display_item_list = item_list

        self.update_table_view_item()

    def filter_type(self, idx: int):
        self.update_table_view_item()

    def update_table_view_item(self):
        self.display_item_list = self.filter_item()
        self._update_table_view_item()

    def _update_table_view_item(self):
        item_model = InventoryTableModel(self.display_item_list)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(item_model)

        self.items_table_view.setModel(proxy_model)
        self.items_table_view.setSortingEnabled(True)
        self.items_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.items_table_view.resizeColumnsToContents()

    def filter_item(self) -> List[DnfItemSlot]:
        show_blank = self.show_blank_chkbox.isChecked()
        select_idx = self.type_combox.currentIndex()
        select_type = type_keys[select_idx]

        # force show blank slot ignore
        if select_idx == 0:
            return list(filter(lambda x: x.type == 0, self.item_list))

        if select_type == 0xFF:
            if show_blank:
                return self.item_list
            else:
                return list(filter(lambda x: x.type != 0x00, self.item_list))

        return list(filter(lambda x: x.type == select_type, self.item_list))

    def on_row_clicked(self, index: QModelIndex):
        selected_item = index.data(Qt.ItemDataRole.UserRole)
        # show empty view
        if selected_item.id == 0:
            self.form_stack_widget.setCurrentIndex(0)
            return

        if selected_item.is_equipment:
            self.form_stack_widget.setCurrentIndex(1)
            self.equipment_form.set_item(selected_item)
        else:
            self.form_stack_widget.setCurrentIndex(2)
            self.stackable_form.set_item(selected_item)

    def refresh(self):
        self.on_refresh.emit()

    def save(self, new_item: DnfItemSlot):
        self.on_save.emit(new_item)

    def delete(self, item: DnfItemSlot):
        self.on_delete.emit(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    item_svc = ItemService()
    ci = item_svc.get_current_character_inventory()
    w = InventoryWidget(ci.backpack)
    w.show()

    w.on_save.connect(lambda it: print('save', it))
    w.on_delete.connect(lambda it: print('delete', it))

    process_id = os.getpid()
    print(f'process id: {process_id}')
    sys.exit(app.exec())
