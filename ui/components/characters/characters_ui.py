# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'characters.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_characters(object):
    def setupUi(self, characters):
        if not characters.objectName():
            characters.setObjectName(u"characters")
        characters.resize(821, 520)
        self.horizontalLayout = QHBoxLayout(characters)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_group_box = QGroupBox(characters)
        self.search_group_box.setObjectName(u"search_group_box")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_group_box.sizePolicy().hasHeightForWidth())
        self.search_group_box.setSizePolicy(sizePolicy)
        self.search_group_box.setBaseSize(QSize(240, 0))
        self.formLayout = QFormLayout(self.search_group_box)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(8, 8, 8, 8)
        self.name_label = QLabel(self.search_group_box)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(self.search_group_box)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.btn_group = QWidget(self.search_group_box)
        self.btn_group.setObjectName(u"btn_group")
        self.horizontalLayout_7 = QHBoxLayout(self.btn_group)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.reset_btn = QPushButton(self.btn_group)
        self.reset_btn.setObjectName(u"reset_btn")

        self.horizontalLayout_7.addWidget(self.reset_btn)

        self.search_btn = QPushButton(self.btn_group)
        self.search_btn.setObjectName(u"search_btn")

        self.horizontalLayout_7.addWidget(self.search_btn)


        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.btn_group)


        self.horizontalLayout.addWidget(self.search_group_box)

        self.character_group_box = QGroupBox(characters)
        self.character_group_box.setObjectName(u"character_group_box")
        self.verticalLayout = QVBoxLayout(self.character_group_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.character_table_view = QTableView(self.character_group_box)
        self.character_table_view.setObjectName(u"character_table_view")
        self.character_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.character_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.character_table_view.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.character_table_view)


        self.horizontalLayout.addWidget(self.character_group_box)


        self.retranslateUi(characters)

        QMetaObject.connectSlotsByName(characters)
    # setupUi

    def retranslateUi(self, characters):
        characters.setWindowTitle(QCoreApplication.translate("characters", u"Form", None))
        self.search_group_box.setTitle(QCoreApplication.translate("characters", u"\u641c\u7d22", None))
        self.name_label.setText(QCoreApplication.translate("characters", u"Name", None))
        self.reset_btn.setText(QCoreApplication.translate("characters", u"Reset", None))
        self.search_btn.setText(QCoreApplication.translate("characters", u"Search", None))
        self.character_group_box.setTitle(QCoreApplication.translate("characters", u"\u5f53\u524d\u89d2\u8272", None))
    # retranslateUi

