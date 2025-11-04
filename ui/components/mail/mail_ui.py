# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mail.ui'
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
    QStackedWidget, QTableView, QVBoxLayout, QWidget)

class Ui_mail(object):
    def setupUi(self, mail):
        if not mail.objectName():
            mail.setObjectName(u"mail")
        mail.resize(985, 826)
        self.horizontalLayout = QHBoxLayout(mail)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mail_list_groupbox = QGroupBox(mail)
        self.mail_list_groupbox.setObjectName(u"mail_list_groupbox")
        self.verticalLayout = QVBoxLayout(self.mail_list_groupbox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.mail_table_view = QTableView(self.mail_list_groupbox)
        self.mail_table_view.setObjectName(u"mail_table_view")
        self.mail_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.mail_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout.addWidget(self.mail_table_view)

        self.action_buttons = QWidget(self.mail_list_groupbox)
        self.action_buttons.setObjectName(u"action_buttons")
        self.horizontalLayout_2 = QHBoxLayout(self.action_buttons)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.refresh_btn = QPushButton(self.action_buttons)
        self.refresh_btn.setObjectName(u"refresh_btn")

        self.horizontalLayout_2.addWidget(self.refresh_btn)

        self.del_btn = QPushButton(self.action_buttons)
        self.del_btn.setObjectName(u"del_btn")

        self.horizontalLayout_2.addWidget(self.del_btn)


        self.verticalLayout.addWidget(self.action_buttons)


        self.horizontalLayout.addWidget(self.mail_list_groupbox)

        self.mail_form = QGroupBox(mail)
        self.mail_form.setObjectName(u"mail_form")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mail_form.sizePolicy().hasHeightForWidth())
        self.mail_form.setSizePolicy(sizePolicy)
        self.mail_form.setMinimumSize(QSize(360, 0))
        self.mail_form.setMaximumSize(QSize(360, 16777215))
        self.mail_form.setBaseSize(QSize(360, 0))
        self.verticalLayout_2 = QVBoxLayout(self.mail_form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.stackedWidget = QStackedWidget(self.mail_form)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.verticalLayout_2.addWidget(self.stackedWidget)

        self.button_group = QWidget(self.mail_form)
        self.button_group.setObjectName(u"button_group")
        self.gridLayout = QGridLayout(self.button_group)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.send_to_current_character_btn = QPushButton(self.button_group)
        self.send_to_current_character_btn.setObjectName(u"send_to_current_character_btn")
        self.send_to_current_character_btn.setAutoDefault(False)

        self.gridLayout.addWidget(self.send_to_current_character_btn, 0, 0, 1, 1)

        self.send_to_online_character_btn = QPushButton(self.button_group)
        self.send_to_online_character_btn.setObjectName(u"send_to_online_character_btn")

        self.gridLayout.addWidget(self.send_to_online_character_btn, 0, 1, 1, 1)

        self.send_to_all_character_btn = QPushButton(self.button_group)
        self.send_to_all_character_btn.setObjectName(u"send_to_all_character_btn")

        self.gridLayout.addWidget(self.send_to_all_character_btn, 1, 0, 1, 1)

        self.delete_all_mail_btn = QPushButton(self.button_group)
        self.delete_all_mail_btn.setObjectName(u"delete_all_mail_btn")

        self.gridLayout.addWidget(self.delete_all_mail_btn, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.button_group)


        self.horizontalLayout.addWidget(self.mail_form)


        self.retranslateUi(mail)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(mail)
    # setupUi

    def retranslateUi(self, mail):
        mail.setWindowTitle(QCoreApplication.translate("mail", u"Form", None))
        self.mail_list_groupbox.setTitle(QCoreApplication.translate("mail", u"\u5f53\u524d\u89d2\u8272\u90ae\u4ef6\u5217\u8868", None))
        self.refresh_btn.setText(QCoreApplication.translate("mail", u"Refresh", None))
        self.del_btn.setText(QCoreApplication.translate("mail", u"Delete Selected", None))
        self.mail_form.setTitle(QCoreApplication.translate("mail", u"\u53d1\u9001\u90ae\u4ef6", None))
        self.send_to_current_character_btn.setText(QCoreApplication.translate("mail", u"\u53d1\u9001\u5f53\u524d\u89d2\u8272", None))
        self.send_to_online_character_btn.setText(QCoreApplication.translate("mail", u"\u53d1\u9001\u5728\u7ebf\u89d2\u8272", None))
        self.send_to_all_character_btn.setText(QCoreApplication.translate("mail", u"\u53d1\u9001\u6240\u6709\u89d2\u8272", None))
        self.delete_all_mail_btn.setText(QCoreApplication.translate("mail", u"\u6e05\u7a7a\u5168\u670d\u90ae\u4ef6", None))
    # retranslateUi

