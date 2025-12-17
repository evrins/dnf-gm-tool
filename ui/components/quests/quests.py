from typing import List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QWidget

from config import config
from dnf_db.entity.signals import gs
from dnf_db.service.quest_service import (
    CharacterQuest,
    Quest,
    QuestService,
)
from ui.components.quests.quests_ui import Ui_quests


class QuestTableModel(QAbstractTableModel):
    def __init__(self, data: List[Quest]):
        super().__init__()
        self._data = data
        self._headers = [
            'idx',
            'id',
            'name',
            'status',
            'type_',
        ]
        self._display_headers = [
            '序号',
            '任务 ID',
            '任务名',
            '状态',
            '类型',
        ]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            key = self._headers[index.column()]
            return row.__dict__[key]
        elif role == Qt.ItemDataRole.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._display_headers[section]
        return None

    def flags(self, index) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class Quests(QWidget, Ui_quests):
    cq: CharacterQuest

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.quest_service = QuestService()

        self.refresh_btn.clicked.connect(self.refresh)

        self.complete_select_btn.clicked.connect(self.complete_select)
        self.complete_all_btn.clicked.connect(self.complete_all)

        self.cancel_select_btn.clicked.connect(self.cancel_select)
        self.cancel_all_btn.clicked.connect(self.cancel_all)

        self.quest_table_view.clicked.connect(self.on_row_click)

        gs.character_no_changed.connect(self.refresh)

        self.refresh()

    def refresh(self):
        if not config.have_valid_account_id_and_character_no():
            return
        self.cq = self.quest_service.get_current_character_quest()

        table_model = QuestTableModel(self.cq.quest_list)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.quest_table_view.setModel(proxy_model)
        self.quest_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.quest_table_view.resizeColumnsToContents()

    def complete_select(self):
        selected_indexes = self.quest_table_view.selectedIndexes()
        if not selected_indexes:
            return
        row: Quest = selected_indexes[0].data(Qt.ItemDataRole.UserRole)
        self.quest_service.complete_current_character_quest(row)
        self.refresh()

    def complete_all(self):
        self.quest_service.complete_current_character_all_quests(self.cq)
        self.refresh()

    def cancel_select(self):
        selected_indexes = self.quest_table_view.selectedIndexes()
        if not selected_indexes:
            return
        row: Quest = selected_indexes[0].data(Qt.ItemDataRole.UserRole)
        self.quest_service.cancel_current_character_quest_by_idx(row.idx)
        self.refresh()

    def cancel_all(self):
        self.quest_service.cancel_current_character_all_quests()
        self.refresh()

    def on_row_click(self, index: QModelIndex):
        row: Quest = index.data(Qt.ItemDataRole.UserRole)

        if row.id == 0 or row.invalid:
            self.quest_text_edit.setText('')
            return

        # set quest detail
        self.quest_text_edit.setText(row.detail)
