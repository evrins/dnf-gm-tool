from typing import List

from PySide6.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QWidget

import config.config
from dnf_db.entity.mail_form_item import MailFormItem, MailItemType
from dnf_db.entity.mail_list_item import MailListItem
from dnf_db.entity.mail_submit_item import MailSubmitItem
from dnf_db.entity.signals import gs
from dnf_db.service.account_service import AccountService
from dnf_db.service.mail_service import MailService
from ui.components.mail.equipment_form import EquipmentForm
from ui.components.mail.mail_ui import Ui_mail
from ui.components.mail.stackable_form import StackableForm


class MailTableModel(QAbstractTableModel):
    def __init__(self, data: List[MailListItem]):
        super().__init__()
        self._data = data
        self._headers = [
            'postal_id',
            'item_id',
            'item_name',
            'num',
            'item_type',
            'sender_name',
        ]
        self._display_headers = [
            '邮件 ID',
            '物品 ID',
            '名称',
            '数量',
            '类型',
            '发送人',
        ]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            key = self._headers[index.column()]
            if key == 'item_type':
                return str(row.item_type)
            else:
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


class Mail(QWidget, Ui_mail):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_item_type = None

        gs.submit_mail_form.connect(self.on_submit)
        gs.character_no_changed.connect(self.refresh)

        self.refresh_btn.clicked.connect(self.refresh)
        self.del_btn.clicked.connect(self.delete_selected)

        self.send_to_current_character_btn.clicked.connect(
            self.send_to_current_character
        )
        self.send_to_online_character_btn.clicked.connect(self.send_to_online_character)
        self.send_to_all_character_btn.clicked.connect(self.send_to_all_character)
        self.delete_all_mail_btn.clicked.connect(self.delete_all_mail)

        self.stackable_form = StackableForm()
        self.stackedWidget.addWidget(self.stackable_form)

        self.equipment_form = EquipmentForm()
        self.stackedWidget.addWidget(self.equipment_form)

        self.stackedWidget.setCurrentIndex(1)

        self.mail_service = MailService()
        self.account_service = AccountService()

        self.refresh()

    def on_submit(self, mail_submit_item: MailSubmitItem):
        self.current_item_type = mail_submit_item.item_type
        if self.current_item_type == MailItemType.Stackable:
            self.stackable_form.set_item(mail_submit_item)
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.equipment_form.set_item(mail_submit_item)
            self.stackedWidget.setCurrentIndex(1)

    def refresh(self):
        self.set_data()

    def send_to_current_character(self):
        current_character_no = config.config.get_current_character_no()
        self._send_to_characters([current_character_no])

    def send_to_online_character(self):
        character_list = self.account_service.get_online_character_list()
        character_no_list = [it.character_no for it in character_list]
        self._send_to_characters(character_no_list)

    def send_to_all_character(self):
        character_list = self.account_service.get_all_valid_character_list()
        character_no_list = [it.character_no for it in character_list]
        self._send_to_characters(character_no_list)

    def _send_to_characters(self, character_no_list: List[int]):
        if not self.current_item_type:
            return
        mail_form_item: MailFormItem = self.stackedWidget.currentWidget().get_item()

        for character_no in character_no_list:
            self.mail_service.send_mail('hello', 'world', character_no, mail_form_item)
        self.refresh()

    def delete_selected(self):
        selected_indexes = self.mail_table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected = selected_indexes[0]
        row = selected.data(Qt.ItemDataRole.UserRole)
        self.mail_service.delete_by_mail_list_item(row)
        self.refresh()

    def delete_all_mail(self):
        self.mail_service.delete_all()

    def set_data(self):
        data = self.mail_service.get_current_character_postal()
        table_model = MailTableModel(data)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.mail_table_view.setModel(proxy_model)
        self.mail_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.mail_table_view.resizeColumnsToContents()
