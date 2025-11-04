from typing import List

from PySide6.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QWidget

from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot
from dnfpkgtool.db.service.item_service import ItemService
from ui.account_cargo_ui import Ui_account_cargo


class AccountCargoModel(QAbstractTableModel):
    def __init__(self, data: List[DnfItemSlot]):
        super().__init__()
        self._data = data
        self._headers = [
            'display_idx',
            'display_name',
            'num_grade',
            'display_rarity_name',
        ]
        self._headers_display = ['ID', '名称', '数量', '稀有度']

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
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers_display[section]
        return None

    def flags(self, index) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class AccountCargo(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_account_cargo()
        self.ui.setupUi(self)

        self.account_cargo_svc = ItemService()

        table_model = AccountCargoModel(
            self.account_cargo_svc.get_current_account_cargo()
        )

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)

        self.ui.table_view.setModel(proxy_model)
        self.ui.table_view.setSortingEnabled(True)
        self.ui.table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.ui.table_view.resizeColumnsToContents()
