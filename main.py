import os
import signal
import sys
from pathlib import Path
from typing import Callable, List

from loguru import logger
from pydantic import BaseModel
from PySide6.QtCore import Qt, QTimer, QCoreApplication, QStandardPaths
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

import resources.resources_rc  # noqa: F401
from config import config
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from dnfpkgtool.db.entity.signals import gs
from startup_check import check_database, check_parquet_files
from ui.components.character_info.character_info import CharacterInfoWidget
from ui.components.characters.characters import Characters
from ui.components.equipment_search.equipment_search import EquipmentSearch
from ui.components.mail.mail import Mail
from ui.components.quests.quests import Quests
from ui.components.settings.settings import Setting
from ui.components.stackable_search.stackable_search import StackableSearch
from ui.inventory_tabview import InventoryTabView

shutdown_requested = False

QCoreApplication.setOrganizationDomain('hu.evrins')
QCoreApplication.setApplicationName('dnf-gm-tool')


def handle_shutdown_signal(sig, frame=None):
    global shutdown_requested
    logger.info(f'signal {sig} received')
    shutdown_requested = True


req_database = 1
req_pvf = 2
req_character_selected = 4


class TabConfig(BaseModel):
    index: int
    name: str
    requires: int
    tab_class: Callable
    # 页面初始化标记
    success_init: bool = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.db_ready = check_database()
        self.parquet_ready = check_parquet_files()
        self.have_user_selected = config.have_valid_account_id_and_character_no()

        self.tab_configs: List[TabConfig] = [
            TabConfig(
                index=0, name='👥 角色列表', requires=req_database, tab_class=Characters
            ),
            TabConfig(
                index=1,
                name='👤 角色信息',
                requires=req_database | req_pvf | req_character_selected,
                tab_class=CharacterInfoWidget,
            ),
            TabConfig(
                index=2, name='🛡️ 装备搜索', requires=req_pvf, tab_class=EquipmentSearch
            ),
            TabConfig(
                index=3, name='📦 物品搜索', requires=req_pvf, tab_class=StackableSearch
            ),
            TabConfig(
                index=4,
                name='🎒 物品',
                requires=req_database | req_pvf | req_character_selected,
                tab_class=InventoryTabView,
            ),
            TabConfig(
                index=5,
                name='📧 邮件',
                requires=req_database | req_pvf | req_character_selected,
                tab_class=Mail,
            ),
            TabConfig(
                index=6,
                name='📜 任务',
                requires=req_database | req_pvf | req_character_selected,
                tab_class=Quests,
            ),
            TabConfig(index=7, name='⚙️ 设置', requires=0, tab_class=Setting),
        ]

        self.create_tabs()
        # Set up status bar
        self.status_bar = self.statusBar()
        self.update_status_message()

        # Connect signals
        gs.db_config_changed.connect(self.handle_db_config_change)
        gs.pvf_changed.connect(self.handle_pvf_change)
        gs.character_no_changed.connect(self.handle_character_no_change)
        gs.submit_mail_form.connect(self.handle_submit_to_mail)
        gs.character_no_changed.connect(self.update_status_message)

        # Set window properties
        self.setWindowTitle('DNF GM Tool')
        self.resize(1200, 820)  # Set initial size

        # set default tab
        self.tab_widget.setCurrentIndex(0)

        self.quit_timer = QTimer(self)
        self.quit_timer.setInterval(1000)
        self.quit_timer.timeout.connect(self.check_for_shutdown)
        self.quit_timer.start()

    def create_not_ready_widget(self, error_msg: str) -> QWidget:
        layout = QVBoxLayout()
        label = QLabel()
        label.setText(error_msg)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)
        return container

    def create_tabs(self):
        for it in self.tab_configs:
            self.create_tab(it)

    def create_tab(self, it: TabConfig):
        if it.success_init:
            return
        if it.requires & req_database and not self.db_ready:
            tab = self.create_not_ready_widget(
                '此页面需要可用的数据库连接配置, 请在设置页面配置'
            )
        elif it.requires & req_pvf and not self.parquet_ready:
            tab = self.create_not_ready_widget('此页面需要 pvf 文件, 请在设置页面配置')
        elif it.requires & req_character_selected and not self.have_user_selected:
            tab = self.create_not_ready_widget(
                '此页面需要选中用户, 请在角色列表页面选择'
            )
        else:
            tab = it.tab_class()
            it.success_init = True

        # already exists replace it if not success inited
        if it.index < self.tab_widget.count():
            self.tab_widget.removeTab(it.index)
            self.tab_widget.insertTab(it.index, tab, it.name)
        else:
            self.tab_widget.addTab(tab, it.name)

    def handle_db_config_change(self):
        self.db_ready = True
        self.create_tabs()

    def handle_pvf_change(self):
        self.parquet_ready = True
        self.create_tabs()

    def handle_character_no_change(self):
        self.have_user_selected = True
        self.create_tabs()

    def handle_submit_to_mail(self, mail_submit_item: MailSubmitItem):
        self.tab_widget.setCurrentIndex(5)  # index of mail tab

    def update_status_message(self):
        account_id = config.get_current_account_id()
        character_no = config.get_current_character_no()
        character_name = config.get_config().character_name

        if account_id == 0 or character_no == 0:
            msg = '无选中角色'
        else:
            msg = f'当前角色 [{character_no}] {character_name}'

        self.status_bar.showMessage(msg)

    def closeEvent(self, event):
        """Handle application close event."""
        # The tab widget will automatically handle closing its child widgets
        event.accept()

    def check_for_shutdown(self):
        if shutdown_requested:
            logger.info('Shutdown requested, closing application')
            self.close()


def is_running_as_windows_executable() -> bool:
    return sys.platform == 'win32' and getattr(sys, 'frozen', False)


def is_running_as_macos_app() -> bool:
    return sys.platform == 'darwin' and getattr(sys, 'frozen', False)


def start_app():
    if is_running_as_windows_executable():
        base_dir = Path(__file__).parent.parent
        config.set_base_dir(base_dir)
    elif is_running_as_macos_app():
        app_data_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        config.set_base_dir(Path(app_data_path))

    config.init_dirs()

    config.load()

    logger.add(config.get_log_dir() / 'app.log', rotation='10 MB')

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    app = QApplication(sys.argv)

    if sys.platform == 'darwin':
        app.setWindowIcon(QIcon(':/icon.icns'))
    elif sys.platform == 'win32':
        app.setWindowIcon(QIcon(':/icon.ico'))

    app.setStyle('Fusion')
    mw = MainWindow()
    mw.show()

    pid = os.getpid()
    logger.info(f'PID: {pid}')

    app.exec()


if __name__ == '__main__':
    start_app()
