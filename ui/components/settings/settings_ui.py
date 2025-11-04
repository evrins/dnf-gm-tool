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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QWidget)

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
        self.formLayout = QFormLayout(self.db_groupbox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(4, 4, 4, 4)
        self.host_label = QLabel(self.db_groupbox)
        self.host_label.setObjectName(u"host_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.host_label)

        self.host_combox = QComboBox(self.db_groupbox)
        self.host_combox.setObjectName(u"host_combox")
        self.host_combox.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.host_combox)

        self.port_label = QLabel(self.db_groupbox)
        self.port_label.setObjectName(u"port_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.port_label)

        self.port_combox = QComboBox(self.db_groupbox)
        self.port_combox.setObjectName(u"port_combox")
        self.port_combox.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.port_combox)

        self.username_label = QLabel(self.db_groupbox)
        self.username_label.setObjectName(u"username_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.username_label)

        self.username_combox = QComboBox(self.db_groupbox)
        self.username_combox.setObjectName(u"username_combox")
        self.username_combox.setEditable(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.username_combox)

        self.password_label = QLabel(self.db_groupbox)
        self.password_label.setObjectName(u"password_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.password_label)

        self.password_combox = QComboBox(self.db_groupbox)
        self.password_combox.setObjectName(u"password_combox")
        self.password_combox.setEditable(True)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.password_combox)

        self.status_label = QLabel(self.db_groupbox)
        self.status_label.setObjectName(u"status_label")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.status_label)

        self.status_text_label = QLabel(self.db_groupbox)
        self.status_text_label.setObjectName(u"status_text_label")
        self.status_text_label.setStyleSheet(u"            QLabel {\n"
"                padding: 8px;\n"
"                border: 1px solid #ccc;\n"
"                border-radius: 4px;\n"
"                background-color: #f5f5f5;\n"
"                color: #666;\n"
"            }")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.status_text_label)

        self.save_btn = QPushButton(self.db_groupbox)
        self.save_btn.setObjectName(u"save_btn")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.save_btn)


        self.horizontalLayout.addWidget(self.db_groupbox)

        self.pvf_groupbox = QGroupBox(settings)
        self.pvf_groupbox.setObjectName(u"pvf_groupbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pvf_groupbox.sizePolicy().hasHeightForWidth())
        self.pvf_groupbox.setSizePolicy(sizePolicy1)
        self.formLayout_2 = QFormLayout(self.pvf_groupbox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.pvf_label = QLabel(self.pvf_groupbox)
        self.pvf_label.setObjectName(u"pvf_label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.pvf_label)

        self.pvf_combox = QComboBox(self.pvf_groupbox)
        self.pvf_combox.setObjectName(u"pvf_combox")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.pvf_combox)

        self.select_pvf_btn = QPushButton(self.pvf_groupbox)
        self.select_pvf_btn.setObjectName(u"select_pvf_btn")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.select_pvf_btn)

        self.progress_status = QLabel(self.pvf_groupbox)
        self.progress_status.setObjectName(u"progress_status")
        self.progress_status.setWordWrap(True)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.progress_status)


        self.horizontalLayout.addWidget(self.pvf_groupbox)

        self.other_groupbox = QGroupBox(settings)
        self.other_groupbox.setObjectName(u"other_groupbox")

        self.horizontalLayout.addWidget(self.other_groupbox)


        self.retranslateUi(settings)

        QMetaObject.connectSlotsByName(settings)
    # setupUi

    def retranslateUi(self, settings):
        settings.setWindowTitle(QCoreApplication.translate("settings", u"Form", None))
        self.db_groupbox.setTitle(QCoreApplication.translate("settings", u"Database", None))
        self.host_label.setText(QCoreApplication.translate("settings", u"Host", None))
        self.port_label.setText(QCoreApplication.translate("settings", u"Port", None))
        self.username_label.setText(QCoreApplication.translate("settings", u"Username", None))
        self.password_label.setText(QCoreApplication.translate("settings", u"Password", None))
        self.status_label.setText(QCoreApplication.translate("settings", u"Status", None))
        self.status_text_label.setText(QCoreApplication.translate("settings", u"Ready", None))
        self.save_btn.setText(QCoreApplication.translate("settings", u"Test && Save", None))
        self.pvf_groupbox.setTitle(QCoreApplication.translate("settings", u"PVF", None))
        self.pvf_label.setText(QCoreApplication.translate("settings", u"PVF", None))
        self.select_pvf_btn.setText(QCoreApplication.translate("settings", u"Select PVF", None))
        self.progress_status.setText(QCoreApplication.translate("settings", u"Progress", None))
        self.other_groupbox.setTitle(QCoreApplication.translate("settings", u"Others", None))
    # retranslateUi

