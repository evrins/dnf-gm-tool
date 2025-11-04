# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inventory.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGroupBox, QHBoxLayout, QHeaderView, QPushButton,
    QSizePolicy, QStackedWidget, QTableView, QVBoxLayout,
    QWidget)

class Ui_inventory_container(object):
    def setupUi(self, inventory_container):
        if not inventory_container.objectName():
            inventory_container.setObjectName(u"inventory_container")
        inventory_container.resize(917, 749)
        self.horizontalLayout = QHBoxLayout(inventory_container)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.table_view_container = QGroupBox(inventory_container)
        self.table_view_container.setObjectName(u"table_view_container")
        self.verticalLayout = QVBoxLayout(self.table_view_container)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.widget = QWidget(self.table_view_container)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.show_blank_chkbox = QCheckBox(self.widget)
        self.show_blank_chkbox.setObjectName(u"show_blank_chkbox")

        self.horizontalLayout_2.addWidget(self.show_blank_chkbox)

        self.type_combox = QComboBox(self.widget)
        self.type_combox.setObjectName(u"type_combox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_combox.sizePolicy().hasHeightForWidth())
        self.type_combox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.type_combox)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widget_2)

        self.refresh_btn = QPushButton(self.widget)
        self.refresh_btn.setObjectName(u"refresh_btn")

        self.horizontalLayout_2.addWidget(self.refresh_btn)

        self.show_blank_chkbox.raise_()
        self.type_combox.raise_()
        self.refresh_btn.raise_()
        self.widget_2.raise_()

        self.verticalLayout.addWidget(self.widget)

        self.items_table_view = QTableView(self.table_view_container)
        self.items_table_view.setObjectName(u"items_table_view")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.items_table_view.sizePolicy().hasHeightForWidth())
        self.items_table_view.setSizePolicy(sizePolicy2)
        self.items_table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.items_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.items_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout.addWidget(self.items_table_view)


        self.horizontalLayout.addWidget(self.table_view_container)

        self.item_edit = QGroupBox(inventory_container)
        self.item_edit.setObjectName(u"item_edit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.item_edit.sizePolicy().hasHeightForWidth())
        self.item_edit.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.item_edit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.form_stack_widget = QStackedWidget(self.item_edit)
        self.form_stack_widget.setObjectName(u"form_stack_widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.form_stack_widget.sizePolicy().hasHeightForWidth())
        self.form_stack_widget.setSizePolicy(sizePolicy4)

        self.verticalLayout_2.addWidget(self.form_stack_widget)


        self.horizontalLayout.addWidget(self.item_edit)


        self.retranslateUi(inventory_container)

        self.form_stack_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(inventory_container)
    # setupUi

    def retranslateUi(self, inventory_container):
        inventory_container.setWindowTitle(QCoreApplication.translate("inventory_container", u"Form", None))
        self.table_view_container.setTitle(QCoreApplication.translate("inventory_container", u"Current Items", None))
        self.show_blank_chkbox.setText(QCoreApplication.translate("inventory_container", u"Show Blank", None))
        self.refresh_btn.setText(QCoreApplication.translate("inventory_container", u"Refresh", None))
        self.item_edit.setTitle(QCoreApplication.translate("inventory_container", u"Item Edit", None))
    # retranslateUi

