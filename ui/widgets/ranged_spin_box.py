from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QWidget


class RangedSpinBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ranged_spinbox_layout = QHBoxLayout()
        ranged_spinbox_layout.setSpacing(5)  # Set spacing between widgets
        ranged_spinbox_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins to match other fields

        self.min_level_spinbox = QSpinBox()
        self.min_level_spinbox.setRange(0, 100)
        self.min_level_spinbox.setValue(0)
        self.min_level_spinbox.setSingleStep(1)

        # Add text label between spinboxes
        level_separator = QLabel('to')
        level_separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_separator.setStyleSheet('QLabel { margin: 0 3px; font-weight: normal; }')

        self.max_level_spinbox = QSpinBox()
        self.max_level_spinbox.setRange(0, 100)
        self.max_level_spinbox.setValue(0)
        self.max_level_spinbox.setSingleStep(1)

        # Add widgets with equal stretch for spinboxes
        ranged_spinbox_layout.addWidget(self.min_level_spinbox, 1)
        ranged_spinbox_layout.addWidget(level_separator, 0)
        ranged_spinbox_layout.addWidget(self.max_level_spinbox, 1)

        self.setLayout(ranged_spinbox_layout)
