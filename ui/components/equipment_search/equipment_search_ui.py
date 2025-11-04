# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equipment_search.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableView,
    QTextEdit, QVBoxLayout, QWidget)

from ui.widgets.ranged_spin_box import RangedSpinBox

class Ui_equipment_search(object):
    def setupUi(self, equipment_search):
        if not equipment_search.objectName():
            equipment_search.setObjectName(u"equipment_search")
        equipment_search.resize(956, 599)
        self.horizontalLayout = QHBoxLayout(equipment_search)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_form = QGroupBox(equipment_search)
        self.search_form.setObjectName(u"search_form")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_form.sizePolicy().hasHeightForWidth())
        self.search_form.setSizePolicy(sizePolicy)
        self.search_form.setBaseSize(QSize(240, 0))
        self.formLayout = QFormLayout(self.search_form)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(8, 8, 8, 8)
        self.name_label = QLabel(self.search_form)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(self.search_form)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.main_label = QLabel(self.search_form)
        self.main_label.setObjectName(u"main_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.main_label)

        self.main_combox = QComboBox(self.search_form)
        self.main_combox.setObjectName(u"main_combox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.main_combox)

        self.minor_label = QLabel(self.search_form)
        self.minor_label.setObjectName(u"minor_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.minor_label)

        self.minor_combox = QComboBox(self.search_form)
        self.minor_combox.setObjectName(u"minor_combox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.minor_combox)

        self.rarity_label = QLabel(self.search_form)
        self.rarity_label.setObjectName(u"rarity_label")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.rarity_label)

        self.rarity_combox = QComboBox(self.search_form)
        self.rarity_combox.setObjectName(u"rarity_combox")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.rarity_combox)

        self.level_label = QLabel(self.search_form)
        self.level_label.setObjectName(u"level_label")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.level_label)

        self.ranged_spinbox = RangedSpinBox(self.search_form)
        self.ranged_spinbox.setObjectName(u"ranged_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ranged_spinbox.sizePolicy().hasHeightForWidth())
        self.ranged_spinbox.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.ranged_spinbox)

        self.search_btn = QPushButton(self.search_form)
        self.search_btn.setObjectName(u"search_btn")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.search_btn)

        self.submit_btn = QPushButton(self.search_form)
        self.submit_btn.setObjectName(u"submit_btn")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.submit_btn)

        self.patch_label = QLabel(self.search_form)
        self.patch_label.setObjectName(u"patch_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.patch_label)

        self.patch_combox = QComboBox(self.search_form)
        self.patch_combox.setObjectName(u"patch_combox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.patch_combox)


        self.horizontalLayout.addWidget(self.search_form)

        self.search_results = QGroupBox(equipment_search)
        self.search_results.setObjectName(u"search_results")
        self.verticalLayout = QVBoxLayout(self.search_results)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.result_table_view = QTableView(self.search_results)
        self.result_table_view.setObjectName(u"result_table_view")
        self.result_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.result_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.result_table_view.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.result_table_view)


        self.horizontalLayout.addWidget(self.search_results)

        self.detail = QGroupBox(equipment_search)
        self.detail.setObjectName(u"detail")
        self.verticalLayout_2 = QVBoxLayout(self.detail)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.detail_text_edit = QTextEdit(self.detail)
        self.detail_text_edit.setObjectName(u"detail_text_edit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.detail_text_edit.sizePolicy().hasHeightForWidth())
        self.detail_text_edit.setSizePolicy(sizePolicy2)
        self.detail_text_edit.setBaseSize(QSize(240, 0))
        self.detail_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.detail_text_edit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.detail_text_edit)


        self.horizontalLayout.addWidget(self.detail)


        self.retranslateUi(equipment_search)

        QMetaObject.connectSlotsByName(equipment_search)
    # setupUi

    def retranslateUi(self, equipment_search):
        equipment_search.setWindowTitle(QCoreApplication.translate("equipment_search", u"Form", None))
        self.search_form.setTitle(QCoreApplication.translate("equipment_search", u"Form", None))
        self.name_label.setText(QCoreApplication.translate("equipment_search", u"Name", None))
        self.main_label.setText(QCoreApplication.translate("equipment_search", u"Main", None))
        self.minor_label.setText(QCoreApplication.translate("equipment_search", u"Minor", None))
        self.rarity_label.setText(QCoreApplication.translate("equipment_search", u"Rarity", None))
        self.level_label.setText(QCoreApplication.translate("equipment_search", u"Level", None))
        self.search_btn.setText(QCoreApplication.translate("equipment_search", u"Search", None))
        self.submit_btn.setText(QCoreApplication.translate("equipment_search", u"Send to Mail", None))
        self.patch_label.setText(QCoreApplication.translate("equipment_search", u"Patch", None))
        self.search_results.setTitle(QCoreApplication.translate("equipment_search", u"Results", None))
        self.detail.setTitle(QCoreApplication.translate("equipment_search", u"Detail", None))
        self.detail_text_edit.setPlaceholderText(QCoreApplication.translate("equipment_search", u"select equipment to show detail", None))
    # retranslateUi

