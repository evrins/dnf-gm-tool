# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stackable_search.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

from ui.widgets.ranged_spin_box import RangedSpinBox

class Ui_stackable_search(object):
    def setupUi(self, stackable_search):
        if not stackable_search.objectName():
            stackable_search.setObjectName(u"stackable_search")
        stackable_search.resize(967, 678)
        self.horizontalLayout = QHBoxLayout(stackable_search)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.form_group = QGroupBox(stackable_search)
        self.form_group.setObjectName(u"form_group")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form_group.sizePolicy().hasHeightForWidth())
        self.form_group.setSizePolicy(sizePolicy)
        self.form_group.setBaseSize(QSize(240, 0))
        self.formLayout = QFormLayout(self.form_group)
        self.formLayout.setObjectName(u"formLayout")
        self.name_label = QLabel(self.form_group)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(self.form_group)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.category_label = QLabel(self.form_group)
        self.category_label.setObjectName(u"category_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.category_label)

        self.category_combox = QComboBox(self.form_group)
        self.category_combox.setObjectName(u"category_combox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.category_combox)

        self.rarity_label = QLabel(self.form_group)
        self.rarity_label.setObjectName(u"rarity_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.rarity_label)

        self.rarity_combox = QComboBox(self.form_group)
        self.rarity_combox.setObjectName(u"rarity_combox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.rarity_combox)

        self.level_label = QLabel(self.form_group)
        self.level_label.setObjectName(u"level_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.level_label)

        self.ranged_spinbox = RangedSpinBox(self.form_group)
        self.ranged_spinbox.setObjectName(u"ranged_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ranged_spinbox.sizePolicy().hasHeightForWidth())
        self.ranged_spinbox.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.ranged_spinbox)

        self.search_btn = QPushButton(self.form_group)
        self.search_btn.setObjectName(u"search_btn")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.search_btn)

        self.submit_btn = QPushButton(self.form_group)
        self.submit_btn.setObjectName(u"submit_btn")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.submit_btn)


        self.horizontalLayout.addWidget(self.form_group)

        self.result_group = QGroupBox(stackable_search)
        self.result_group.setObjectName(u"result_group")
        self.verticalLayout = QVBoxLayout(self.result_group)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.result_table_view = QTableView(self.result_group)
        self.result_table_view.setObjectName(u"result_table_view")
        self.result_table_view.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.result_table_view)


        self.horizontalLayout.addWidget(self.result_group)


        self.retranslateUi(stackable_search)

        QMetaObject.connectSlotsByName(stackable_search)
    # setupUi

    def retranslateUi(self, stackable_search):
        stackable_search.setWindowTitle(QCoreApplication.translate("stackable_search", u"Form", None))
        self.form_group.setTitle(QCoreApplication.translate("stackable_search", u"Form", None))
        self.name_label.setText(QCoreApplication.translate("stackable_search", u"Name", None))
        self.category_label.setText(QCoreApplication.translate("stackable_search", u"Category", None))
        self.rarity_label.setText(QCoreApplication.translate("stackable_search", u"Rarity", None))
        self.level_label.setText(QCoreApplication.translate("stackable_search", u"Level", None))
        self.search_btn.setText(QCoreApplication.translate("stackable_search", u"Search", None))
        self.submit_btn.setText(QCoreApplication.translate("stackable_search", u"Send to Mail", None))
        self.result_group.setTitle(QCoreApplication.translate("stackable_search", u"Results", None))
    # retranslateUi

