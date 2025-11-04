from time import time

from loguru import logger
from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QMessageBox,
    QWidget,
)

from config import config
from dnfpkgtool.db import check_mysql_config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.equipment_repo import build_equipment_repo_parquet
from dnfpkgtool.repo.magic_seal_repo import build_magic_seal_parquet
from dnfpkgtool.repo.orb_repo import build_orb_repo_parquet
from dnfpkgtool.repo.skill_repo import build_skill_repo_parquet, get_skill_repo
from dnfpkgtool.repo.stackable_repo import (
    build_stackable_repo_parquet,
    get_stackable_repo,
)
from ui.components.settings.settings_ui import Ui_settings
from util import calculate_hash_of_file


class BuilderThread(QThread):
    progress = Signal(str)
    finished = Signal(bool)

    def __init__(self, pvf_path: str, pvf_hash: str, parent=None):
        super().__init__(parent)
        self.start_time = None
        self.pvf_path = pvf_path
        self.pvf_hash = pvf_hash

    def run(self):
        self.start_time = time()

        if config.create_pvf_dir(self.pvf_hash):
            self.progress.emit(
                f'{self.elapsed():.2f}s: pvf dir already created skip build'
            )
            config.set_pvf_hash(self.pvf_hash)
            self.finished.emit(True)
            return

        try:
            self.progress.emit(f'{self.elapsed():.2f}s: Start building repo parquet')
            reader = PVFReader(self.pvf_path)

            self.progress.emit(
                f'{self.elapsed():.2f}s: Start building equipment repo 1/5'
            )
            build_equipment_repo_parquet(
                reader.get_equipment_dict(),
                config.build_equipment_parquet_file_path(self.pvf_hash),
            )
            self.progress.emit(
                f'{self.elapsed():.2f}s: End building equipment repo 1/5'
            )

            self.progress.emit(
                f'{self.elapsed():.2f}s: Start building stackable repo 2/5'
            )
            build_stackable_repo_parquet(
                reader.get_stackable_dict(),
                config.build_stackable_parquet_file_path(self.pvf_hash),
            )
            self.progress.emit(
                f'{self.elapsed():.2f}s: End building stackable repo 2/5'
            )

            self.progress.emit(
                f'{self.elapsed():.2f}s: Start building magic seal repo 3/5'
            )
            build_magic_seal_parquet(
                reader.get_magic_seal_dict(),
                config.build_magic_seal_parquet_file_path(self.pvf_hash),
            )
            self.progress.emit(
                f'{self.elapsed():.2f}s: End building magic seal repo 3/5'
            )

            self.progress.emit(f'{self.elapsed():.2f}s: Start building skill repo 4/5')
            build_skill_repo_parquet(
                reader.get_skill_list(),
                config.build_skill_parquet_parquet_file_path(self.pvf_hash),
            )
            self.progress.emit(
                f'{self.elapsed():.2f}s: End building magic seal repo 4/5'
            )

            # build orb repo should come after stackable_repo and skill_repo
            self.progress.emit(f'{self.elapsed():.2f}s: Start building orb repo 5/5')
            stackable_repo = get_stackable_repo()
            skill_repo = get_skill_repo()
            build_orb_repo_parquet(
                stackable_repo,
                skill_repo,
                config.build_orb_parquet_file_path(self.pvf_hash),
            )
            reader.close()
            self.progress.emit(f'{self.elapsed():.2f}s: End building orb repo 5/5')
            config.set_pvf_hash(self.pvf_hash)

            self.progress.emit(f'{self.elapsed():.2f}s: End building repo parquet')
            self.finished.emit(True)
        except Exception as e:
            logger.error(f'fail to build parquet: {e}')
            self.finished.emit(False)

    def elapsed(self) -> float:
        return time() - self.start_time if self.start_time else 0.0


class Setting(QWidget, Ui_settings):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

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

        # load pvf hash
        self.pvf_combox.addItems(history.pvf_hash_list)
        self.pvf_combox.setCurrentText(cfg.pvf_hash)
        self.pvf_combox.currentTextChanged.connect(self.current_pvf_changed)

        self.save_btn.clicked.connect(self.save_and_test)

        self.select_pvf_btn.clicked.connect(self.handle_add_pvf)

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

        # Test connection
        try:
            valid = check_mysql_config(host, port, username, password)

            if valid:
                self._show_success_status('Success')
                self._save_settings(host, port, username, password)
            else:
                self._show_error_status('Failed')

        except Exception as e:
            self._show_error_status(f'Connection error: {str(e)}')

        finally:
            # Re-enable button after test
            QTimer.singleShot(100, lambda: self.save_btn.setEnabled(True))

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
            self, 'Select PVF', '', 'All Files (*.*);;Pvf Files (*.pvf)'
        )
        if not file_name:
            logger.warning('No file selected')
            return
        logger.info(f'selected file: {file_name}')
        self.pvf_hash = calculate_hash_of_file(file_name)

        self.builder_thread = BuilderThread(file_name, self.pvf_hash)
        self.progress = []
        self.pvf_combox.setEnabled(False)
        self.select_pvf_btn.setEnabled(False)

        self.builder_thread.progress.connect(self.update_progress)
        self.builder_thread.finished.connect(self.builder_finished)

        self.builder_thread.start()

    def update_progress(self, status: str):
        self.progress.append(status)

        self.progress_status.setText('\n'.join(self.progress))

    def builder_finished(self, success: bool):
        self.pvf_combox.setEnabled(True)
        self.select_pvf_btn.setEnabled(True)
        if not success:
            return

        if self.pvf_combox.findText(self.pvf_hash) == -1:
            self.pvf_combox.addItem(self.pvf_hash)

    def current_pvf_changed(self, pvf_hash: str):
        config.set_pvf_hash(pvf_hash)
