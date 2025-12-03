import json
from typing import Dict

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
    QTimer,
)
from PySide6.QtWidgets import (
    QWidget,
)

from dnfpkgtool.db.entity.mail_form_item import MailItemType
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.repo.repo_manager import get_stackable_repo
from dnfpkgtool.repo.stackable_repo import StackableRepo
from ui.components.stackable_search.stackable_search_ui import Ui_stackable_search
from ui.components.stackable_search.vars import (
    categoryed_stackable_type_dict,
    item_category_key_list,
    item_rarity_list,
)


class StackableTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = [
            'id',
            'name',
            'display_stackable_type',
            'minimum_level',
            'display_rarity',
        ]
        self._display_headers = ['ID', '名称', '物品种类', '等级', '稀有度']

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            key = self._headers[index.column()]
            return self._data[index.row()][key]
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


class StackableSearch(QWidget, Ui_stackable_search):
    stackable_repo: StackableRepo

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_stackable_repo()
        gs.pvf_changed.connect(self.set_stackable_repo)

        self.name_line_edit.returnPressed.connect(self.do_search)

        self.category_combox.addItem('---')
        self.category_combox.addItems(item_category_key_list)

        self.rarity_combox.addItem('---')
        self.rarity_combox.addItems(item_rarity_list)

        self.search_btn.clicked.connect(self.do_search)

        self.submit_btn.clicked.connect(self.submit_to_mail)

    def _adjust_table_columns(self):
        """Adjust table column widths to content."""
        self.result_table_view.resizeColumnsToContents()

    def set_stackable_repo(self):
        self.stackable_repo = get_stackable_repo()

    def do_search(self, s=None):
        name = self.name_line_edit.text().strip()
        category = self.category_combox.currentText()

        stackable_type_list = categoryed_stackable_type_dict.get(category, None)

        min_level = self.ranged_spinbox.min_level_spinbox.value()
        min_level = None if min_level == 0 else int(min_level)
        max_level = self.ranged_spinbox.max_level_spinbox.value()
        max_level = None if max_level == 0 else int(max_level)

        rarity = self.rarity_combox.currentText()
        rarity = None if rarity == '---' else rarity

        if category == '卡片':
            data = self.stackable_repo.query(
                name,
                item_category_list=stackable_type_list,
                min_level=min_level,
                max_level=max_level,
                display_rarity=rarity,
                limit=1024,
            )
        else:
            data = self.stackable_repo.query(
                name,
                stackable_type_list=stackable_type_list,
                min_level=min_level,
                max_level=max_level,
                display_rarity=rarity,
                limit=1024,
            )
        self.update_title(len(data))
        table_model = StackableTableModel(data)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.result_table_view.setModel(proxy_model)

        self.selection_model = self.result_table_view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)

        self.result_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.result_table_view.resizeColumnsToContents()

        # After search, adjust size to new content
        QTimer.singleShot(100, self._adjust_table_columns)

    def submit_to_mail(self):
        selected_indexes = self.result_table_view.selectedIndexes()
        if not selected_indexes:
            return
        row = selected_indexes[0].data(Qt.ItemDataRole.UserRole)
        mail_submit_item = MailSubmitItem(
            item_id=row['id'],
            item_name=row['name'],
            item_type=MailItemType.Stackable,
            stack_limit=row['stack_limit'],
        )
        gs.submit_mail_form.emit(mail_submit_item)

    def update_title(self, n_result: int):
        title = '结果'
        if n_result > 1000:
            title = f'找到 {title} 1000+ 条记录'
        elif n_result > 0:
            title = f'找到 {title} {n_result} 条记录'
        self.result_group.setTitle(title)

    def on_selection_changed(self, selected, deselected):
        indent = ' ' * 4
        rows = self.selection_model.selectedRows()

        if rows:
            row = rows[0].data(Qt.ItemDataRole.UserRole)
            detail = self.render_detail(row)
            self.detail_text_edit.setPlainText(detail)

    def render_detail(self, stackable: Dict) -> str:
        detail = f"""名称: {stackable['name']}
名称2: {stackable['name2']}
等级: {stackable['minimum_level']}
稀有度: {stackable['display_rarity']}
类型: {stackable['display_stackable_type']}
"""
        return detail
