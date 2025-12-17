import os
from time import time
from traceback import print_exc

import shortuuid
from loguru import logger
from pvf_parser_rs import save_parquet
from PySide6.QtCore import QAbstractTableModel, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QMessageBox,
    QWidget,
)
from showinfm import show_in_file_manager

from config import config
from config.config import Pvf, check_mysql_config, update_pvf_by_uuid
from dnf_db.entity.signals import gs
from pvf.repo.orb_repo import build_orb_repo_parquet
from pvf.repo.skill_repo import SkillRepo
from pvf.repo.stackable_repo import StackableRepo
from ui.components.settings.settings_ui import Ui_settings


class MySQLTestThread(QThread):
    """Worker thread for testing MySQL connection without blocking UI."""

    finished = Signal(bool, str)  # success, error_message

    def __init__(self, host: str, port: int, username: str, password: str, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        try:
            valid = check_mysql_config(
                self.host, self.port, self.username, self.password
            )
            if valid:
                self.finished.emit(True, '')
            else:
                self.finished.emit(False, 'Connection failed')
        except Exception as e:
            self.finished.emit(False, str(e))


class BuilderThread(QThread):
    progress = Signal(str)
    progress_int = Signal(int)
    finished = Signal(bool)

    def __init__(self, pvf_path: str, uuid: str, encoding: int, parent=None):
        super().__init__(parent)
        self.start_time = None
        self.pvf_path = pvf_path
        self.uuid = uuid
        self.encoding = encoding

    def run(self):
        self.start_time = time()
        total = 2
        config.create_pvf_dir(self.uuid)

        try:
            self.progress.emit(f'{self.elapsed():.2f}s: Start building repo parquet')
            pvf_dir = config.build_pvf_dir(self.uuid)

            save_parquet(self.pvf_path, self.encoding, os.fspath(pvf_dir))

            self.progress_int.emit(100 / total)

            # build orb repo should come after stackable_repo and skill_repo
            self.progress.emit(
                f'{self.elapsed():.2f}s: Start building orb repo 2/{total}'
            )
            stackable_repo = StackableRepo(
                config.build_stackable_parquet_file_path(self.uuid)
            )
            skill_repo = SkillRepo(
                config.build_skill_parquet_parquet_file_path(self.uuid)
            )
            build_orb_repo_parquet(
                stackable_repo,
                skill_repo,
                config.build_orb_parquet_file_path(self.uuid),
            )
            self.progress.emit(
                f'{self.elapsed():.2f}s: End building orb repo 2/{total}'
            )
            self.progress_int.emit(200 / total)

            config.set_pvf_uuid(self.uuid)

            self.progress.emit(f'{self.elapsed():.2f}s: End building repo parquet')
            self.finished.emit(True)
        except Exception as e:
            print_exc()
            logger.error(f'fail to build parquet: {e}')
            self.finished.emit(False)

    def elapsed(self) -> float:
        return time() - self.start_time if self.start_time else 0.0


class PvfTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = [
            'uuid',
            'remark',
            'encoding',
        ]
        self._display_headers = ['UUID', '备注', '编码']

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            key = self._headers[index.column()]
            value = self._data[index.row()].model_dump()[key]
            if key == 'encoding':
                return ['繁体-BIG5', '简体-GBK'][value]
            else:
                return value
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


class Setting(QWidget, Ui_settings):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.uuid = ''
        self.select_pvf_file = ''

        # load history database config
        cfg = config.get_config()
        history = cfg.history

        self.host_combox.addItems(history.host_list)
        self.host_combox.setCurrentText(cfg.db_config.host)

        self.port_combox.addItems(map(str, history.port_list))
        self.port_combox.setCurrentText(str(cfg.db_config.port))

        self.username_combox.addItems(history.username_list)
        self.username_combox.setCurrentText(cfg.db_config.username)

        self.password_combox.addItems(history.password_list)
        self.password_combox.setCurrentText(cfg.db_config.password)

        self.update_pvf_table()
        self.select_pvf(cfg.pvf_uuid)

        self.add_new.clicked.connect(self.add_new_pvf)
        self.save_pvf_btn.clicked.connect(self.save_pvf)
        self.delete_pvf_btn.clicked.connect(self.delete_pvf)

        self.save_btn.clicked.connect(self.save_and_test)

        self.progress_bar.setValue(0)

        self.select_pvf_btn.clicked.connect(self.handle_add_pvf)

        self.open_data_dir_btn.clicked.connect(self.open_data_dir)

    def save_and_test(self):
        """Test MySQL connection and provide user feedback."""
        host = self.host_combox.currentText().strip()
        port_text = self.port_combox.currentText().strip()
        username = self.username_combox.currentText().strip()
        password = self.password_combox.currentText().strip()

        # Validate input fields
        if not all([host, port_text, username, password]):
            self._show_error_status('Missing fields')
            return

        try:
            port = int(port_text)
        except ValueError:
            self._show_error_status('Invalid port')
            return

        # Show testing status
        self._show_testing_status()

        # Disable button during test
        self.save_btn.setEnabled(False)

        # Test connection in background thread
        self.mysql_test_thread = MySQLTestThread(host, port, username, password)
        self.mysql_test_thread.finished.connect(
            lambda success, error_msg: self._on_mysql_test_finished(
                success, error_msg, host, port, username, password
            )
        )
        self.mysql_test_thread.start()

    def _on_mysql_test_finished(
        self,
        success: bool,
        error_msg: str,
        host: str,
        port: int,
        username: str,
        password: str,
    ):
        """Handle MySQL test completion."""
        if success:
            self._show_success_status('Success')
            self._save_settings(host, port, username, password)
            gs.db_config_changed.emit()
        else:
            self._show_error_status(error_msg or 'Failed')

        # Re-enable button after test
        self.save_btn.setEnabled(True)

    def _show_testing_status(self):
        """Show testing in progress status."""
        self.status_text_label.setText('🔄 Testing connection...')
        self.status_text_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 1px solid #2196F3;
                border-radius: 4px;
                background-color: #E3F2FD;
                color: #1976D2;
                font-weight: bold;
            }
        """)

    def _show_success_status(self, message: str):
        """Show success status with green styling."""
        self.status_text_label.setText(f'✅ {message}')
        self.status_text_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 1px solid #4CAF50;
                border-radius: 4px;
                background-color: #E8F5E8;
                color: #2E7D32;
                font-weight: bold;
            }
        """)

        # Show success message box
        QMessageBox.information(
            self,
            'Connection Successful',
            'MySQL connection test passed successfully!\nSettings have been saved.',
        )

    def _show_error_status(self, message: str):
        """Show error status with red styling."""
        self.status_text_label.setText(f'❌ {message}')
        self.status_text_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 1px solid #F44336;
                border-radius: 4px;
                background-color: #FFEBEE;
                color: #C62828;
                font-weight: bold;
            }
        """)

        # Show error message box
        QMessageBox.critical(
            self,
            'Connection Failed',
            f'MySQL connection test failed:\n\n{message}\n\nPlease check your database settings and try again.',
        )

    def _save_settings(self, host: str, port: int, username: str, password: str):
        # This could save to a config file, registry, or database
        logger.info(f'Saving settings: {host}:{port} user={username}')
        config.save_db_config(host, port, username, password)

        # Add to combobox history if not already present
        self._add_to_history(self.host_combox, host)
        self._add_to_history(self.port_combox, str(port))
        self._add_to_history(self.username_combox, username)
        self._add_to_history(self.password_combox, password)

    def _add_to_history(self, combobox: QComboBox, value: str):
        """Add value to combobox history if not already present."""
        if combobox.findText(value) == -1:
            combobox.addItem(value)
            combobox.setCurrentText(value)

    def handle_add_pvf(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Select PVF', '', 'Pvf Files (*.pvf)'
        )
        if not file_name:
            logger.warning('No file selected')
            return
        logger.info(f'selected file: {file_name}')
        self.select_pvf_file = file_name
        self.select_pvf_btn.setText('已选择')

    def update_progress(self, status: str):
        self.progress.append(status)

        self.progress_status.setText('\n'.join(self.progress))

    def update_progress_bar(self, p: int):
        self.progress_bar.setValue(p)

    def builder_finished(self, success: bool):
        self.save_pvf_btn.setEnabled(True)
        self.select_pvf_btn.setEnabled(True)
        self.select_pvf_btn.setText('选择 pvf 文件')
        if not success:
            return

        remark = self.remark_line_edit.text()
        encoding = self.encoding_combox.currentIndex()
        config.add_pvf(Pvf(uuid=self.uuid, remark=remark, encoding=encoding))
        self.update_pvf_table()
        self.select_pvf(self.uuid)

    def on_selection_changed(self, selected, deselected):
        rows = self.selection_model.selectedRows()
        if not rows:
            return
        row: Pvf = rows[0].data(Qt.ItemDataRole.UserRole)

        self.uuid = row.uuid
        self.encoding_combox.setCurrentIndex(row.encoding)
        self.remark_line_edit.setText(row.remark)
        config.set_pvf_uuid(row.uuid)

    def add_new_pvf(self):
        self.uuid = ''
        self.select_pvf_file = ''
        self.select_pvf_btn.setText('选择 pvf 文件')
        self.encoding_combox.setCurrentIndex(0)
        self.remark_line_edit.setText('')

    def save_pvf(self):
        self.select_pvf_btn.setEnabled(False)
        self.save_pvf_btn.setEnabled(False)

        # update
        if self.uuid:
            remark = self.remark_line_edit.text()
            update_pvf_by_uuid(self.uuid, remark)
            self.update_pvf_table()
            self.select_pvf(self.uuid)
            self.select_pvf_btn.setEnabled(True)
            self.save_pvf_btn.setEnabled(True)
            # add new
        else:
            self.uuid = shortuuid.uuid()
            encoding = self.encoding_combox.currentIndex()
            self.builder_thread = BuilderThread(
                self.select_pvf_file, self.uuid, encoding + 1
            )
            self.progress = []

            self.progress_bar.setValue(0)
            self.builder_thread.progress_int.connect(self.update_progress_bar)
            self.builder_thread.progress.connect(self.update_progress)
            self.builder_thread.finished.connect(self.builder_finished)

            self.builder_thread.start()

    def delete_pvf(self):
        config.delete_pvf_by_uuid(self.uuid)
        self.update_pvf_table()

    def update_pvf_table(self):
        cfg = config.get_config()

        table_model = PvfTableModel(cfg.pvf_list)
        self.pvf_table_view.setModel(table_model)

        self.selection_model = self.pvf_table_view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)

        self.pvf_table_view.resizeColumnsToContents()

    def select_pvf(self, uuid: str):
        model = self.pvf_table_view.model()
        start_index = model.index(0, 0)

        matches = model.match(
            start_index, Qt.ItemDataRole.DisplayRole, uuid, 1, Qt.MatchFlag.MatchExactly
        )

        if matches:
            found_index = matches[0]
            row_idx = found_index.row()
            self.pvf_table_view.selectRow(row_idx)

    def current_pvf_changed(self, pvf_hash: str):
        config.set_pvf_uuid(pvf_hash)

    def open_data_dir(self):
        show_in_file_manager(config.get_base_dir().__str__())
