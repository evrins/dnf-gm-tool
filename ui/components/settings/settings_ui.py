# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_settings(object):
    def setupUi(self, settings):
        if not settings.objectName():
            settings.setObjectName(u"settings")
        settings.resize(903, 759)
        self.horizontalLayout = QHBoxLayout(settings)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.db_groupbox = QGroupBox(settings)
        self.db_groupbox.setObjectName(u"db_groupbox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.db_groupbox.sizePolicy().hasHeightForWidth())
        self.db_groupbox.setSizePolicy(sizePolicy)
        self.db_groupbox.setMinimumSize(QSize(200, 0))
        self.db_groupbox.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.db_groupbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.widget_2 = QWidget(self.db_groupbox)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMinimumSize(QSize(0, 0))
        self.formLayout_3 = QFormLayout(self.widget_2)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.host_combox = QComboBox(self.widget_2)
        self.host_combox.setObjectName(u"host_combox")
        self.host_combox.setEditable(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.host_combox)

        self.host_label = QLabel(self.widget_2)
        self.host_label.setObjectName(u"host_label")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.host_label)

        self.port_label = QLabel(self.widget_2)
        self.port_label.setObjectName(u"port_label")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.port_label)

        self.port_combox = QComboBox(self.widget_2)
        self.port_combox.setObjectName(u"port_combox")
        self.port_combox.setEditable(True)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.port_combox)

        self.username_label = QLabel(self.widget_2)
        self.username_label.setObjectName(u"username_label")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.username_label)

        self.username_combox = QComboBox(self.widget_2)
        self.username_combox.setObjectName(u"username_combox")
        self.username_combox.setEditable(True)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.username_combox)

        self.password_label = QLabel(self.widget_2)
        self.password_label.setObjectName(u"password_label")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.password_label)

        self.password_combox = QComboBox(self.widget_2)
        self.password_combox.setObjectName(u"password_combox")
        self.password_combox.setEditable(True)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.password_combox)

        self.status_label = QLabel(self.widget_2)
        self.status_label.setObjectName(u"status_label")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.status_label)

        self.status_text_label = QLabel(self.widget_2)
        self.status_text_label.setObjectName(u"status_text_label")
        self.status_text_label.setStyleSheet(u"            QLabel {\n"
"                padding: 8px;\n"
"                border: 1px solid #ccc;\n"
"                border-radius: 4px;\n"
"                background-color: #f5f5f5;\n"
"                color: #666;\n"
"            }")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.status_text_label)

        self.save_btn = QPushButton(self.widget_2)
        self.save_btn.setObjectName(u"save_btn")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.save_btn)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.db_groupbox)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.widget_3)

        self.open_data_dir_btn = QPushButton(self.db_groupbox)
        self.open_data_dir_btn.setObjectName(u"open_data_dir_btn")

        self.verticalLayout_3.addWidget(self.open_data_dir_btn)


        self.horizontalLayout.addWidget(self.db_groupbox)

        self.groupBox = QGroupBox(settings)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.pvf_table_view = QTableView(self.groupBox)
        self.pvf_table_view.setObjectName(u"pvf_table_view")
        self.pvf_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.pvf_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_2.addWidget(self.pvf_table_view)


        self.horizontalLayout.addWidget(self.groupBox)

        self.pvf_groupbox = QGroupBox(settings)
        self.pvf_groupbox.setObjectName(u"pvf_groupbox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pvf_groupbox.sizePolicy().hasHeightForWidth())
        self.pvf_groupbox.setSizePolicy(sizePolicy3)
        self.pvf_groupbox.setMinimumSize(QSize(200, 0))
        self.pvf_groupbox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.pvf_groupbox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.widget = QWidget(self.pvf_groupbox)
        self.widget.setObjectName(u"widget")
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(0, 0))
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.pvf_label = QLabel(self.widget)
        self.pvf_label.setObjectName(u"pvf_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.pvf_label)

        self.select_pvf_btn = QPushButton(self.widget)
        self.select_pvf_btn.setObjectName(u"select_pvf_btn")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.select_pvf_btn)

        self.encoding_label = QLabel(self.widget)
        self.encoding_label.setObjectName(u"encoding_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.encoding_label)

        self.encoding_combox = QComboBox(self.widget)
        self.encoding_combox.addItem("")
        self.encoding_combox.addItem("")
        self.encoding_combox.setObjectName(u"encoding_combox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.encoding_combox)

        self.remark_label = QLabel(self.widget)
        self.remark_label.setObjectName(u"remark_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.remark_label)

        self.remark_line_edit = QLineEdit(self.widget)
        self.remark_line_edit.setObjectName(u"remark_line_edit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.remark_line_edit)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.add_new_btn = QPushButton(self.widget_4)
        self.add_new_btn.setObjectName(u"add_new_btn")

        self.horizontalLayout_2.addWidget(self.add_new_btn)

        self.update_pfv_btn = QPushButton(self.widget_4)
        self.update_pfv_btn.setObjectName(u"update_pfv_btn")

        self.horizontalLayout_2.addWidget(self.update_pfv_btn)

        self.delete_pvf_btn = QPushButton(self.widget_4)
        self.delete_pvf_btn.setObjectName(u"delete_pvf_btn")

        self.horizontalLayout_2.addWidget(self.delete_pvf_btn)


        self.formLayout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.widget_4)


        self.verticalLayout.addWidget(self.widget)

        self.progress_bar = QProgressBar(self.pvf_groupbox)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)

        self.progress_status = QLabel(self.pvf_groupbox)
        self.progress_status.setObjectName(u"progress_status")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.progress_status.sizePolicy().hasHeightForWidth())
        self.progress_status.setSizePolicy(sizePolicy4)
        self.progress_status.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.progress_status.setWordWrap(True)

        self.verticalLayout.addWidget(self.progress_status)


        self.horizontalLayout.addWidget(self.pvf_groupbox)


        self.retranslateUi(settings)

        QMetaObject.connectSlotsByName(settings)
    # setupUi

    def retranslateUi(self, settings):
        settings.setWindowTitle(QCoreApplication.translate("settings", u"Form", None))
        self.db_groupbox.setTitle(QCoreApplication.translate("settings", u"\u6570\u636e\u5e93", None))
        self.host_label.setText(QCoreApplication.translate("settings", u"\u4e3b\u673a", None))
        self.port_label.setText(QCoreApplication.translate("settings", u"\u7aef\u53e3", None))
        self.username_label.setText(QCoreApplication.translate("settings", u"\u7528\u6237", None))
        self.password_label.setText(QCoreApplication.translate("settings", u"\u5bc6\u7801", None))
        self.status_label.setText(QCoreApplication.translate("settings", u"\u72b6\u6001", None))
        self.status_text_label.setText(QCoreApplication.translate("settings", u"\u5c31\u7eea", None))
        self.save_btn.setText(QCoreApplication.translate("settings", u"\u6d4b\u8bd5 \u5e76 \u4fdd\u5b58", None))
        self.open_data_dir_btn.setText(QCoreApplication.translate("settings", u"\u6253\u5f00\u6570\u636e\u76ee\u5f55", None))
        self.groupBox.setTitle(QCoreApplication.translate("settings", u"PVF", None))
        self.pvf_groupbox.setTitle(QCoreApplication.translate("settings", u"\u7f16\u8f91", None))
        self.pvf_label.setText(QCoreApplication.translate("settings", u"PVF", None))
        self.select_pvf_btn.setText(QCoreApplication.translate("settings", u"\u9009\u62e9 pvf \u6587\u4ef6", None))
        self.encoding_label.setText(QCoreApplication.translate("settings", u"\u6587\u672c\u7f16\u7801", None))
        self.encoding_combox.setItemText(0, QCoreApplication.translate("settings", u"\u7e41\u4f53-BIG", None))
        self.encoding_combox.setItemText(1, QCoreApplication.translate("settings", u"\u7b80\u4f53-GBK", None))

        self.remark_label.setText(QCoreApplication.translate("settings", u"\u5907\u6ce8", None))
        self.add_new_btn.setText(QCoreApplication.translate("settings", u"\u65b0\u589e", None))
        self.update_pfv_btn.setText(QCoreApplication.translate("settings", u"\u66f4\u65b0", None))
        self.delete_pvf_btn.setText(QCoreApplication.translate("settings", u"\u5220\u9664", None))
        self.progress_status.setText(QCoreApplication.translate("settings", u"\u8fdb\u5ea6", None))
    # retranslateUi

