# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equipment_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QLabel, QLineEdit, QSizePolicy, QSpinBox,
    QWidget)

class Ui_equipment_form(object):
    def setupUi(self, equipment_form):
        if not equipment_form.objectName():
            equipment_form.setObjectName(u"equipment_form")
        equipment_form.resize(404, 650)
        self.formLayout = QFormLayout(equipment_form)
        self.formLayout.setObjectName(u"formLayout")
        self.id_label = QLabel(equipment_form)
        self.id_label.setObjectName(u"id_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.id_label)

        self.id_line_edit = QLineEdit(equipment_form)
        self.id_line_edit.setObjectName(u"id_line_edit")
        self.id_line_edit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.id_line_edit)

        self.name_label = QLabel(equipment_form)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(equipment_form)
        self.name_line_edit.setObjectName(u"name_line_edit")
        self.name_line_edit.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.seal_label = QLabel(equipment_form)
        self.seal_label.setObjectName(u"seal_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.seal_label)

        self.seal_checkbox = QCheckBox(equipment_form)
        self.seal_checkbox.setObjectName(u"seal_checkbox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.seal_checkbox)

        self.grade_label = QLabel(equipment_form)
        self.grade_label.setObjectName(u"grade_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.grade_label)

        self.grade_spin_box = QSpinBox(equipment_form)
        self.grade_spin_box.setObjectName(u"grade_spin_box")
        self.grade_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.grade_spin_box)

        self.endurance_label = QLabel(equipment_form)
        self.endurance_label.setObjectName(u"endurance_label")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.endurance_label)

        self.endurance_spin_box = QSpinBox(equipment_form)
        self.endurance_spin_box.setObjectName(u"endurance_spin_box")
        self.endurance_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.endurance_spin_box)

        self.reinforce_type_label = QLabel(equipment_form)
        self.reinforce_type_label.setObjectName(u"reinforce_type_label")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.reinforce_type_label)

        self.reinforce_type_combox = QComboBox(equipment_form)
        self.reinforce_type_combox.setObjectName(u"reinforce_type_combox")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.reinforce_type_combox)

        self.reinforce_value_label = QLabel(equipment_form)
        self.reinforce_value_label.setObjectName(u"reinforce_value_label")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.reinforce_value_label)

        self.reinforce_value_spin_box = QSpinBox(equipment_form)
        self.reinforce_value_spin_box.setObjectName(u"reinforce_value_spin_box")
        self.reinforce_value_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.reinforce_value_spin_box)

        self.enhance_level_label = QLabel(equipment_form)
        self.enhance_level_label.setObjectName(u"enhance_level_label")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.enhance_level_label)

        self.enhance_level_spin_box = QSpinBox(equipment_form)
        self.enhance_level_spin_box.setObjectName(u"enhance_level_spin_box")
        self.enhance_level_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.enhance_level_spin_box)

        self.forge_level_label = QLabel(equipment_form)
        self.forge_level_label.setObjectName(u"forge_level_label")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.forge_level_label)

        self.forge_level_spin_box = QSpinBox(equipment_form)
        self.forge_level_spin_box.setObjectName(u"forge_level_spin_box")
        self.forge_level_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.forge_level_spin_box)

        self.gold_label = QLabel(equipment_form)
        self.gold_label.setObjectName(u"gold_label")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.gold_label)

        self.gold_spin_box = QSpinBox(equipment_form)
        self.gold_spin_box.setObjectName(u"gold_spin_box")
        self.gold_spin_box.setMaximum(999999999)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.gold_spin_box)


        self.retranslateUi(equipment_form)

        QMetaObject.connectSlotsByName(equipment_form)
    # setupUi

    def retranslateUi(self, equipment_form):
        equipment_form.setWindowTitle(QCoreApplication.translate("equipment_form", u"Form", None))
        self.id_label.setText(QCoreApplication.translate("equipment_form", u"ID", None))
        self.name_label.setText(QCoreApplication.translate("equipment_form", u"\u540d\u79f0", None))
        self.seal_label.setText(QCoreApplication.translate("equipment_form", u"\u5c01\u88c5", None))
        self.grade_label.setText(QCoreApplication.translate("equipment_form", u"\u54c1\u7ea7", None))
        self.endurance_label.setText(QCoreApplication.translate("equipment_form", u"\u8010\u4e45", None))
        self.reinforce_type_label.setText(QCoreApplication.translate("equipment_form", u"\u589e\u5e45\u7c7b\u578b", None))
        self.reinforce_value_label.setText(QCoreApplication.translate("equipment_form", u"\u589e\u5e45\u503c", None))
        self.enhance_level_label.setText(QCoreApplication.translate("equipment_form", u"\u5f3a\u5316\u7b49\u7ea7", None))
        self.forge_level_label.setText(QCoreApplication.translate("equipment_form", u"\u953b\u9020\u7b49\u7ea7", None))
        self.gold_label.setText(QCoreApplication.translate("equipment_form", u"\u91d1\u94b1", None))
    # retranslateUi

