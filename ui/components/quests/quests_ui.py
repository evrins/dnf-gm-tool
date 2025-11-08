# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'quests.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QTableView, QTextEdit, QVBoxLayout, QWidget)

class Ui_quests(object):
    def setupUi(self, quests):
        if not quests.objectName():
            quests.setObjectName(u"quests")
        quests.resize(727, 586)
        self.horizontalLayout = QHBoxLayout(quests)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.quest_group_box = QGroupBox(quests)
        self.quest_group_box.setObjectName(u"quest_group_box")
        self.verticalLayout = QVBoxLayout(self.quest_group_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.quest_table_view = QTableView(self.quest_group_box)
        self.quest_table_view.setObjectName(u"quest_table_view")
        self.quest_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.quest_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout.addWidget(self.quest_table_view)

        self.btn_group = QWidget(self.quest_group_box)
        self.btn_group.setObjectName(u"btn_group")
        self.gridLayout = QGridLayout(self.btn_group)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.cancel_select_btn = QPushButton(self.btn_group)
        self.cancel_select_btn.setObjectName(u"cancel_select_btn")

        self.gridLayout.addWidget(self.cancel_select_btn, 2, 0, 1, 1)

        self.cancel_all_btn = QPushButton(self.btn_group)
        self.cancel_all_btn.setObjectName(u"cancel_all_btn")

        self.gridLayout.addWidget(self.cancel_all_btn, 2, 1, 1, 1)

        self.complete_all_btn = QPushButton(self.btn_group)
        self.complete_all_btn.setObjectName(u"complete_all_btn")

        self.gridLayout.addWidget(self.complete_all_btn, 1, 1, 1, 1)

        self.complete_select_btn = QPushButton(self.btn_group)
        self.complete_select_btn.setObjectName(u"complete_select_btn")

        self.gridLayout.addWidget(self.complete_select_btn, 1, 0, 1, 1)

        self.refresh_btn = QPushButton(self.btn_group)
        self.refresh_btn.setObjectName(u"refresh_btn")

        self.gridLayout.addWidget(self.refresh_btn, 0, 0, 1, 2)


        self.verticalLayout.addWidget(self.btn_group)


        self.horizontalLayout.addWidget(self.quest_group_box)

        self.detail_group_box = QGroupBox(quests)
        self.detail_group_box.setObjectName(u"detail_group_box")
        self.verticalLayout_2 = QVBoxLayout(self.detail_group_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.quest_text_edit = QTextEdit(self.detail_group_box)
        self.quest_text_edit.setObjectName(u"quest_text_edit")

        self.verticalLayout_2.addWidget(self.quest_text_edit)


        self.horizontalLayout.addWidget(self.detail_group_box)


        self.retranslateUi(quests)

        QMetaObject.connectSlotsByName(quests)
    # setupUi

    def retranslateUi(self, quests):
        quests.setWindowTitle(QCoreApplication.translate("quests", u"Form", None))
        self.quest_group_box.setTitle(QCoreApplication.translate("quests", u"Quests", None))
        self.cancel_select_btn.setText(QCoreApplication.translate("quests", u"Cancel Select", None))
        self.cancel_all_btn.setText(QCoreApplication.translate("quests", u"Cancel All", None))
        self.complete_all_btn.setText(QCoreApplication.translate("quests", u"Complete All", None))
        self.complete_select_btn.setText(QCoreApplication.translate("quests", u"Complete Select", None))
        self.refresh_btn.setText(QCoreApplication.translate("quests", u"Refresh", None))
        self.detail_group_box.setTitle(QCoreApplication.translate("quests", u"Detail", None))
    # retranslateUi

