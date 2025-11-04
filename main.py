import signal
import sys
import tracemalloc

from loguru import logger
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

from config import config
from config.config import get_config
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from dnfpkgtool.db.entity.signals import gs
from ui.components.characters.characters import Characters
from ui.components.equipment_search.equipment_search import EquipmentSearch
from ui.components.mail.mail import Mail
from ui.components.settings.settings import Setting
from ui.components.stackable_search.stackable_search import StackableSearch
from ui.inventory_tabview import InventoryTabView

shutdown_requested = False


def handle_shutdown_signal(sig, frame=None):
    global shutdown_requested
    logger.info(f'signal {sig} received')
    shutdown_requested = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.character_widget = Characters()
        self.tab_widget.addTab(self.character_widget, 'Characters')

        self.equip_search = EquipmentSearch()
        self.tab_widget.addTab(self.equip_search, '🛡️ Equipment Search')

        self.stackable_search = StackableSearch()
        self.tab_widget.addTab(self.stackable_search, '📦 Stackable Search')

        self.inventory_tabview = InventoryTabView()
        self.tab_widget.addTab(self.inventory_tabview, 'Inventory')

        self.mail_widget = Mail()
        self.tab_widget.addTab(self.mail_widget, '📧 Mail')

        self.settings_widget = Setting()
        self.tab_widget.addTab(self.settings_widget, '⚙️ Settings')

        # Set up status bar
        self.status_bar = self.statusBar()
        self.update_status_message()

        # Connect signals
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

    def handle_submit_to_mail(self, mail_submit_item: MailSubmitItem):
        self.tab_widget.setCurrentWidget(self.mail_widget)

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

    def dump_memory(self):
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('traceback')
        print('[ Top 10 memory-allocating lines ]')
        for stat in top_stats[:10]:
            print(stat)


if __name__ == '__main__':
    config.init_dirs()
    tracemalloc.start()

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mw = MainWindow()
    mw.show()

    if get_config().have_valid_pvf():
        gs.pvf_changed.emit()
    app.exec()
