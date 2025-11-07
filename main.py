import signal
import sys
import tracemalloc
from pathlib import Path

from loguru import logger
from PySide6.QtCore import Qt, QTimer
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
from ui.components.characters.characters import Characters
from ui.components.equipment_search.equipment_search import EquipmentSearch
from ui.components.mail.mail import Mail
from ui.components.quests.quests import Quests
from ui.components.settings.settings import Setting
from ui.components.stackable_search.stackable_search import StackableSearch
from ui.inventory_tabview import InventoryTabView

shutdown_requested = False


def handle_shutdown_signal(sig, frame=None):
    global shutdown_requested
    logger.info(f'signal {sig} received')
    shutdown_requested = True


TAB_CHARACTERS = '👥 Characters'
TAB_CHARACTERS_INDEX = 0
TAB_EQUIPMENT_SEARCH = '🛡️ Equipment Search'
TAB_EQUIPMENT_SEARCH_INDEX = 1
TAB_STACKABLE_SEARCH = '📦 Stackable Search'
TAB_STACKABLE_SEARCH_INDEX = 2
TAB_INVENTORY = '🎒 Inventory'
TAB_INVENTORY_INDEX = 3
TAB_MAIL = '📧 Mail'
TAB_MAIL_INDEX = 4
TAB_QUEST = '📜 Quest'
TAB_QUEST_INDEX = 5
TAB_SETTINGS = '⚙️ Settings'
TAB_SETTINGS_INDEX = 6


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.db_ready = check_database()
        self.parquet_ready = check_parquet_files()

        if self.db_ready:
            self.character_widget = Characters()
        else:
            self.character_widget = self.create_not_ready_widget(
                'Database not ready, setup in settings tab'
            )

        self.tab_widget.addTab(self.character_widget, TAB_CHARACTERS)

        if self.parquet_ready:
            self.equip_search = EquipmentSearch()
        else:
            self.equip_search = self.create_not_ready_widget(
                'PVF data not ready, setup in settings tab'
            )
        self.tab_widget.addTab(self.equip_search, TAB_EQUIPMENT_SEARCH)

        if self.parquet_ready:
            self.stackable_search = StackableSearch()
        else:
            self.stackable_search = self.create_not_ready_widget(
                'PVF data not ready, setup in settings tab'
            )
        self.tab_widget.addTab(self.stackable_search, TAB_STACKABLE_SEARCH)

        if self.db_ready and self.parquet_ready:
            self.inventory_tabview = InventoryTabView()
        else:
            self.inventory_tabview = self.create_not_ready_widget(
                'Database or PVF data not ready, setup in settings tab'
            )
        self.tab_widget.addTab(self.inventory_tabview, TAB_INVENTORY)

        if self.db_ready and self.parquet_ready:
            self.mail_widget = Mail()
        else:
            self.mail_widget = self.create_not_ready_widget(
                'Database or PVF data not ready, setup in settings tab'
            )
        self.tab_widget.addTab(self.mail_widget, TAB_MAIL)

        if self.db_ready and self.parquet_ready:
            self.quest_widget = Quests()
        else:
            self.quest_widget = self.create_not_ready_widget(
                'Database or PVF data not ready, setup in settings tab'
            )
        self.tab_widget.addTab(self.quest_widget, TAB_QUEST)

        self.settings_widget = Setting()
        self.tab_widget.addTab(self.settings_widget, TAB_SETTINGS)

        # Set up status bar
        self.status_bar = self.statusBar()
        self.update_status_message()

        # Connect signals
        gs.db_config_changed.connect(self.handle_db_config_change)
        gs.pvf_changed.connect(self.handle_pvf_change)
        gs.submit_mail_form.connect(self.handle_submit_to_mail)
        gs.character_no_changed.connect(self.update_status_message)

        # Set window properties
        self.setWindowTitle('DNF GM Tool')
        self.resize(1200, 800)  # Set initial size

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

    def handle_db_config_change(self):
        self.db_ready = True
        self.character_widget = Characters()
        self.tab_widget.removeTab(TAB_CHARACTERS_INDEX)
        self.tab_widget.insertTab(
            TAB_CHARACTERS_INDEX, self.character_widget, TAB_CHARACTERS
        )

        if self.db_ready and self.parquet_ready:
            self.replace_widgets()

    def handle_pvf_change(self):
        self.parquet_ready = True
        self.equip_search = EquipmentSearch()
        self.tab_widget.removeTab(TAB_EQUIPMENT_SEARCH_INDEX)
        self.tab_widget.insertTab(
            TAB_EQUIPMENT_SEARCH_INDEX, self.equip_search, TAB_EQUIPMENT_SEARCH
        )

        self.stackable_search = StackableSearch()
        self.tab_widget.removeTab(TAB_STACKABLE_SEARCH_INDEX)
        self.tab_widget.insertTab(
            TAB_STACKABLE_SEARCH_INDEX, self.stackable_search, TAB_STACKABLE_SEARCH
        )

        if self.db_ready and self.parquet_ready:
            self.replace_widgets()

    def replace_widgets(self):
        self.inventory_tabview = InventoryTabView()
        self.tab_widget.removeTab(TAB_INVENTORY_INDEX)
        self.tab_widget.insertTab(
            TAB_INVENTORY_INDEX, self.inventory_tabview, TAB_INVENTORY
        )

        self.mail_widget = Mail()
        self.tab_widget.removeTab(TAB_MAIL_INDEX)
        self.tab_widget.insertTab(TAB_MAIL_INDEX, self.mail_widget, TAB_MAIL)

        self.quest_widget = Quests()
        self.tab_widget.removeTab(TAB_QUEST_INDEX)
        self.tab_widget.insertTab(TAB_QUEST_INDEX, self.quest_widget, TAB_QUEST)

    def handle_submit_to_mail(self, mail_submit_item: MailSubmitItem):
        self.tab_widget.setCurrentIndex(TAB_MAIL_INDEX)

    def update_status_message(self):
        account_id = config.get_current_account_id()
        character_no = config.get_current_character_no()
        character_name = config.get_config().character_name

        if account_id == 0 or character_no == 0:
            msg = 'No Character Selected'
        else:
            msg = f'Current Character [{character_no}] {character_name}'

        self.status_bar.showMessage(msg)

    def closeEvent(self, event):
        """Handle application close event."""
        # The tab widget will automatically handle closing its child widgets
        event.accept()

    def check_for_shutdown(self):
        if shutdown_requested:
            logger.info('Shutdown requested, closing application')
            self.close()


if __name__ == '__main__':
    base_dir = Path(__file__).parent
    config.set_base_dir(base_dir)

    config.init_dirs()

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

    app.exec()
