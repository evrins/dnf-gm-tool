from PySide6.QtWidgets import QWidget

from ui.components.inventory.empty_ui import Ui_empty


class Empty(QWidget, Ui_empty):
    def __init__(self, /, parent=None):
        super().__init__(parent)
        self.setupUi(self)
