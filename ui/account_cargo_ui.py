# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'account_cargo.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtWidgets import (
    QTableView,
    QVBoxLayout,
)


class Ui_account_cargo(object):
    def setupUi(self, account_cargo):
        if not account_cargo.objectName():
            account_cargo.setObjectName('account_cargo')
        account_cargo.resize(569, 566)
        self.verticalLayout = QVBoxLayout(account_cargo)
        self.verticalLayout.setObjectName('verticalLayout')
        self.table_view = QTableView(account_cargo)
        self.table_view.setObjectName('table_view')

        self.verticalLayout.addWidget(self.table_view)

        self.retranslateUi(account_cargo)

        QMetaObject.connectSlotsByName(account_cargo)

    # setupUi

    def retranslateUi(self, account_cargo):
        account_cargo.setWindowTitle(
            QCoreApplication.translate('account_cargo', 'Form', None)
        )

    # retranslateUi
