# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stackable_form.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QSpinBox, QWidget)

class Ui_stackable_form(object):
    def setupUi(self, stackable_form):
        if not stackable_form.objectName():
            stackable_form.setObjectName(u"stackable_form")
        stackable_form.resize(400, 300)
        self.formLayout = QFormLayout(stackable_form)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(8, 8, 8, 8)
        self.id_label = QLabel(stackable_form)
        self.id_label.setObjectName(u"id_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.id_label)

        self.id_line_edit = QLineEdit(stackable_form)
        self.id_line_edit.setObjectName(u"id_line_edit")
        self.id_line_edit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.id_line_edit)

        self.name_label = QLabel(stackable_form)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(stackable_form)
        self.name_line_edit.setObjectName(u"name_line_edit")
        self.name_line_edit.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.num_label = QLabel(stackable_form)
        self.num_label.setObjectName(u"num_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.num_label)

        self.num_spin_box = QSpinBox(stackable_form)
        self.num_spin_box.setObjectName(u"num_spin_box")
        self.num_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.num_spin_box)

        self.gold_label = QLabel(stackable_form)
        self.gold_label.setObjectName(u"gold_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.gold_label)

        self.gold_spin_box = QSpinBox(stackable_form)
        self.gold_spin_box.setObjectName(u"gold_spin_box")
        self.gold_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.gold_spin_box)


        self.retranslateUi(stackable_form)

        QMetaObject.connectSlotsByName(stackable_form)
    # setupUi

    def retranslateUi(self, stackable_form):
        stackable_form.setWindowTitle(QCoreApplication.translate("stackable_form", u"Form", None))
        self.id_label.setText(QCoreApplication.translate("stackable_form", u"ID", None))
        self.name_label.setText(QCoreApplication.translate("stackable_form", u"\u540d\u79f0", None))
        self.num_label.setText(QCoreApplication.translate("stackable_form", u"\u6570\u91cf", None))
        self.gold_label.setText(QCoreApplication.translate("stackable_form", u"\u91d1\u94b1", None))
    # retranslateUi

