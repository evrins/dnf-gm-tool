import json

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

from dnfpkgtool.db.entity.mail_form_item import ItemType
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.repo.equipment_repo import EquipmentRepo, get_equipment_repo
from ui.components.equipment_search.equipment_search_ui import Ui_equipment_search
from ui.components.stackable_search.vars import (
    default_options,
    equipment_name_mapping,
    job_name_mapping,
    main_options,
    minor_options,
    patch_options,
    rarity_list,
)


class EquipmentTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = [
            'id',
            'name',
            'display_equipment_type',
            'display_usable_job',
            'level',
            'display_rarity',
        ]
        self._headers_display = ['ID', '名称', '装备类型', '可用职业', '等级', '稀有度']

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
                return self._headers_display[section]
        return None

    def flags(self, index) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class EquipmentSearch(QWidget, Ui_equipment_search):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.equipment_repo: EquipmentRepo = None

        gs.pvf_changed.connect(self.set_equipment_repo)

        self.name_line_edit.returnPressed.connect(self.do_search)
        self.main_combox.addItems(main_options)
        self.main_combox.currentTextChanged.connect(self.main_option_changed)

        self.minor_combox.addItems(default_options)
        self.minor_combox.setEnabled(False)
        self.minor_combox.currentTextChanged.connect(self.minor_option_changed)

        self.patch_combox.addItems(default_options)
        self.patch_combox.setEnabled(False)

        self.rarity_combox.addItem('---')
        self.rarity_combox.addItems(rarity_list)

        self.search_btn.clicked.connect(self.do_search)

        self.submit_btn.clicked.connect(self.submit_to_mail)

        self.result_table_view.clicked.connect(self.on_row_clicked)

    def set_equipment_repo(self):
        self.equipment_repo = get_equipment_repo()

    def _adjust_table_columns(self):
        """Adjust table column widths to content."""
        self.result_table_view.resizeColumnsToContents()

    def adjust_size_to_content(self):
        """Public method to adjust table columns to content."""
        self._adjust_table_columns()

    def main_option_changed(self, text: str):
        next_minor_options = minor_options.get(text, default_options)
        enable_minor_option = next_minor_options != default_options

        self.minor_combox.clear()
        self.minor_combox.addItems(next_minor_options)
        self.minor_combox.setEnabled(enable_minor_option)

    def minor_option_changed(self, text: str):
        key = f'{self.main_combox.currentText()}/{text}'
        next_patch_options = patch_options.get(key, default_options)
        enable_patch_option = next_patch_options != default_options

        self.patch_combox.clear()
        self.patch_combox.addItems(next_patch_options)
        self.patch_combox.setEnabled(enable_patch_option)

    def do_search(self, s=None):
        name = self.name_line_edit.text().strip()
        main_option = self.main_combox.currentText()
        minor_option = self.minor_combox.currentText()
        patch_option = self.patch_combox.currentText()

        equipment_type_list = None
        usable_job = None
        item_group_name = None
        armor_type = None

        if main_option == '---':
            equipment_type_list = None
        elif main_option == '武器':
            equipment_type_list = ['[weapon]']
            usable_job = job_name_mapping[minor_option]
            item_group_name = equipment_name_mapping[patch_option]
        elif main_option == '防具':
            selected_equipment_type = equipment_name_mapping[patch_option]
            if selected_equipment_type is None:
                equipment_type_list = [
                    '[coat]',
                    '[waist]',
                    '[shoulder]',
                    '[shoes]',
                    '[pants]',
                ]
            else:
                equipment_type_list = [selected_equipment_type]
            armor_type = equipment_name_mapping[minor_option]
        elif main_option == '首饰':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = ['[amulet]', '[wrist]', '[ring]']
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '特殊装备':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = ['[support]', '[magic stone]']
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '装扮':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = [
                    '[aurora avatar]',
                    '[hair avatar]',
                    '[hat avatar]',
                    '[face avatar]',
                    '[breast avatar]',
                    '[coat avatar]',
                    '[skin avatar]',
                    '[waist avatar]',
                    '[pants avatar]',
                    '[shoes avatar]',
                ]
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '宠物':
            equipment_type_list = ['[creature]']
        elif main_option == '称号':
            equipment_type_list = ['[title name]']
        elif main_option == '宠物装备':
            equipment_type_list = [
                '[artifact blue]',
                '[artifact green]',
                '[artifact red]',
            ]
        elif main_option == '契约效果':
            equipment_type_list = ['']
        else:
            raise Exception(f'unknown main option: {main_option}')

        min_level = self.ranged_spinbox.min_level_spinbox.value()
        min_level = None if min_level == 0 else int(min_level)
        max_level = self.ranged_spinbox.max_level_spinbox.value()
        max_level = None if max_level == 0 else int(max_level)

        rarity = self.rarity_combox.currentText()
        rarity = None if rarity == '---' else rarity

        data = self.equipment_repo.query(
            name,
            equipment_type_list,
            usable_job,
            item_group_name,
            armor_type,
            min_level=min_level,
            max_level=max_level,
            rarity=rarity,
            limit=1024,
        )
        self.update_title(len(data))
        table_model = EquipmentTableModel(data)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.result_table_view.setModel(proxy_model)
        self.result_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # Adjust table columns to content
        QTimer.singleShot(100, self._adjust_table_columns)

    def submit_to_mail(self):
        selected_indexes = self.result_table_view.selectedIndexes()
        if not selected_indexes:
            return
        row = selected_indexes[0].data(Qt.ItemDataRole.UserRole)
        mail_submit_item = MailSubmitItem(
            item_id=row['id'],
            item_name=row['name'],
            item_type=ItemType.Equipment,
            endurance=row['durability'],
            sub_type=row['sub_type'],
        )

        equipment_type = row['equipment_type']
        if equipment_type in [
            '[aurora avatar]',
            '[hair avatar]',
            '[hat avatar]',
            '[face avatar]',
            '[breast avatar]',
            '[coat avatar]',
            '[skin avatar]',
            '[waist avatar]',
            '[pants avatar]',
            '[shoes avatar]',
        ]:
            mail_submit_item.item_type = ItemType.Avatar
        elif equipment_type in ['[creature]']:
            mail_submit_item.item_type = ItemType.Creature

        gs.submit_mail_form.emit(mail_submit_item)

    def on_row_clicked(self, index: QModelIndex):
        row = index.data(Qt.ItemDataRole.UserRole)
        indent = ' ' * 4
        json_string = row['json']
        d = json.loads(json_string)
        lines = []
        for k, v in d.items():
            lines.append(k)
            if (
                k == '[basic explain]'
                or k == '[detail explain]'
                or k == '[flavor text]'
            ):
                if v:
                    for it in v:
                        for sub in it.split('\r\n'):
                            sub = sub.strip()
                            lines.append(f'{indent}{sub}')
                else:
                    lines.append('')
            else:
                lines.append(f'{indent}{v}')
        content = '\n'.join(lines)
        self.detail_text_edit.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.detail_text_edit.setText(content)

    def update_title(self, n_result: int):
        title = 'Results'
        if n_result > 1000:
            title = f'{title} 1000+ records found'
        elif n_result > 0:
            title = f'{title} {n_result} records found'
        self.search_results.setTitle(title)
