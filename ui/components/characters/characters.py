from typing import List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QWidget

from config import config
from dnfpkgtool.db.entity.character_list_item import CharacterListItem
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.db.service.account_service import AccountService
from ui.components.characters.characters_ui import Ui_characters


class CharacterTableModel(QAbstractTableModel):
    def __init__(self, data: List[CharacterListItem]):
        super().__init__()
        self._data = data
        self._headers = [
            'account_id',
            'character_no',
            'character_name',
            'online_text',
            'level',
            'job',
            'expert_job',
        ]
        self._headers_display = [
            '账户 ID',
            '角色No.',
            '角色名称',
            '在线状态',
            '等级',
            '职业',
            '副职业',
        ]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            key = self._headers[index.column()]
            row = self._data[index.row()]
            if key == 'online_text':
                return row.online_text
            else:
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


class Characters(QWidget, Ui_characters):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.account_service = AccountService()

        self.reset_btn.clicked.connect(self.reset)
        self.search_btn.clicked.connect(self.search_characters)
        self.name_line_edit.returnPressed.connect(self.search_characters)

        self.character_table_view.clicked.connect(self.on_row_click)

        gs.character_info_changed.connect(self.search_characters)
        self.reset()

    def reset(self):
        self.name_line_edit.setText('')
        self.search_characters()

    def search_characters(self):
        character_list = self.account_service.search_characters(
            self.name_line_edit.text()
        )
        table_model = CharacterTableModel(character_list)
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.character_table_view.setModel(proxy_model)
        self.character_table_view.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.character_table_view.resizeColumnsToContents()

    def on_row_click(self, index: QModelIndex):
        row: CharacterListItem = index.data(Qt.ItemDataRole.UserRole)
        config.set_account_id_and_character_no(
            row.account_id, row.character_no, row.character_name
        )
