# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'character_info.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_character_info(object):
    def setupUi(self, character_info):
        if not character_info.objectName():
            character_info.setObjectName(u"character_info")
        character_info.resize(1275, 725)
        self.gridLayout = QGridLayout(character_info)
        self.gridLayout.setObjectName(u"gridLayout")
        self.points_group_box = QGroupBox(character_info)
        self.points_group_box.setObjectName(u"points_group_box")
        self.points_group_box.setMinimumSize(QSize(200, 0))
        self.points_group_box.setMaximumSize(QSize(200, 16777215))
        self.formLayout_4 = QFormLayout(self.points_group_box)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(8, 8, 8, 8)
        self.cash_cera_label = QLabel(self.points_group_box)
        self.cash_cera_label.setObjectName(u"cash_cera_label")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.cash_cera_label)

        self.cash_cera_spin_box = QDoubleSpinBox(self.points_group_box)
        self.cash_cera_spin_box.setObjectName(u"cash_cera_spin_box")
        self.cash_cera_spin_box.setReadOnly(True)
        self.cash_cera_spin_box.setDecimals(0)
        self.cash_cera_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cash_cera_spin_box)

        self.cash_cera_point_label = QLabel(self.points_group_box)
        self.cash_cera_point_label.setObjectName(u"cash_cera_point_label")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.cash_cera_point_label)

        self.cash_cera_point_spin_box = QDoubleSpinBox(self.points_group_box)
        self.cash_cera_point_spin_box.setObjectName(u"cash_cera_point_spin_box")
        self.cash_cera_point_spin_box.setReadOnly(True)
        self.cash_cera_point_spin_box.setDecimals(0)
        self.cash_cera_point_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cash_cera_point_spin_box)

        self.sp_label = QLabel(self.points_group_box)
        self.sp_label.setObjectName(u"sp_label")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.sp_label)

        self.sp_spin_box = QDoubleSpinBox(self.points_group_box)
        self.sp_spin_box.setObjectName(u"sp_spin_box")
        self.sp_spin_box.setReadOnly(True)
        self.sp_spin_box.setDecimals(0)
        self.sp_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.sp_spin_box)

        self.qp_label = QLabel(self.points_group_box)
        self.qp_label.setObjectName(u"qp_label")

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.LabelRole, self.qp_label)

        self.qp_spin_box = QDoubleSpinBox(self.points_group_box)
        self.qp_spin_box.setObjectName(u"qp_spin_box")
        self.qp_spin_box.setReadOnly(True)
        self.qp_spin_box.setDecimals(0)
        self.qp_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.FieldRole, self.qp_spin_box)

        self.tp_label = QLabel(self.points_group_box)
        self.tp_label.setObjectName(u"tp_label")

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.LabelRole, self.tp_label)

        self.tp_spin_box = QDoubleSpinBox(self.points_group_box)
        self.tp_spin_box.setObjectName(u"tp_spin_box")
        self.tp_spin_box.setReadOnly(True)
        self.tp_spin_box.setDecimals(0)
        self.tp_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.FieldRole, self.tp_spin_box)


        self.gridLayout.addWidget(self.points_group_box, 0, 3, 1, 1)

        self.coin_group_box = QGroupBox(character_info)
        self.coin_group_box.setObjectName(u"coin_group_box")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coin_group_box.sizePolicy().hasHeightForWidth())
        self.coin_group_box.setSizePolicy(sizePolicy)
        self.coin_group_box.setMinimumSize(QSize(200, 0))
        self.coin_group_box.setMaximumSize(QSize(200, 16777215))
        self.formLayout_3 = QFormLayout(self.coin_group_box)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(8, 8, 8, 8)
        self.cargo_coin_label = QLabel(self.coin_group_box)
        self.cargo_coin_label.setObjectName(u"cargo_coin_label")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.cargo_coin_label)

        self.cargo_coin_spin_box = QDoubleSpinBox(self.coin_group_box)
        self.cargo_coin_spin_box.setObjectName(u"cargo_coin_spin_box")
        self.cargo_coin_spin_box.setDecimals(0)
        self.cargo_coin_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cargo_coin_spin_box)

        self.backpack_coin_label = QLabel(self.coin_group_box)
        self.backpack_coin_label.setObjectName(u"backpack_coin_label")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.backpack_coin_label)

        self.backpack_coin_spin_box = QDoubleSpinBox(self.coin_group_box)
        self.backpack_coin_spin_box.setObjectName(u"backpack_coin_spin_box")
        self.backpack_coin_spin_box.setDecimals(0)
        self.backpack_coin_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.backpack_coin_spin_box)

        self.pay_coin_label = QLabel(self.coin_group_box)
        self.pay_coin_label.setObjectName(u"pay_coin_label")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.pay_coin_label)

        self.pay_coin_spin_box = QDoubleSpinBox(self.coin_group_box)
        self.pay_coin_spin_box.setObjectName(u"pay_coin_spin_box")
        self.pay_coin_spin_box.setDecimals(0)
        self.pay_coin_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.pay_coin_spin_box)

        self.save_coin_btn = QPushButton(self.coin_group_box)
        self.save_coin_btn.setObjectName(u"save_coin_btn")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.save_coin_btn)


        self.gridLayout.addWidget(self.coin_group_box, 1, 1, 1, 1)

        self.character_info_group_box = QGroupBox(character_info)
        self.character_info_group_box.setObjectName(u"character_info_group_box")
        sizePolicy.setHeightForWidth(self.character_info_group_box.sizePolicy().hasHeightForWidth())
        self.character_info_group_box.setSizePolicy(sizePolicy)
        self.character_info_group_box.setMinimumSize(QSize(200, 0))
        self.character_info_group_box.setMaximumSize(QSize(200, 16777215))
        self.formLayout = QFormLayout(self.character_info_group_box)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(8, 8, 8, 8)
        self.name_label = QLabel(self.character_info_group_box)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_line_edit = QLineEdit(self.character_info_group_box)
        self.name_line_edit.setObjectName(u"name_line_edit")
        self.name_line_edit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_line_edit)

        self.level_label = QLabel(self.character_info_group_box)
        self.level_label.setObjectName(u"level_label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.level_label)

        self.level_spin_box = QSpinBox(self.character_info_group_box)
        self.level_spin_box.setObjectName(u"level_spin_box")
        self.level_spin_box.setMaximum(200)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.level_spin_box)

        self.role_label = QLabel(self.character_info_group_box)
        self.role_label.setObjectName(u"role_label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.role_label)

        self.role_combox = QComboBox(self.character_info_group_box)
        self.role_combox.setObjectName(u"role_combox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.role_combox)

        self.job_label = QLabel(self.character_info_group_box)
        self.job_label.setObjectName(u"job_label")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.job_label)

        self.job_combox = QComboBox(self.character_info_group_box)
        self.job_combox.setObjectName(u"job_combox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.job_combox)

        self.wake_label = QLabel(self.character_info_group_box)
        self.wake_label.setObjectName(u"wake_label")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.wake_label)

        self.wake_combox = QComboBox(self.character_info_group_box)
        self.wake_combox.setObjectName(u"wake_combox")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.wake_combox)

        self.expert_label = QLabel(self.character_info_group_box)
        self.expert_label.setObjectName(u"expert_label")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.expert_label)

        self.expert_combox = QComboBox(self.character_info_group_box)
        self.expert_combox.setObjectName(u"expert_combox")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.expert_combox)

        self.save_character_info_btn = QPushButton(self.character_info_group_box)
        self.save_character_info_btn.setObjectName(u"save_character_info_btn")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.save_character_info_btn)


        self.gridLayout.addWidget(self.character_info_group_box, 0, 0, 2, 1)

        self.action_button_group_box = QGroupBox(character_info)
        self.action_button_group_box.setObjectName(u"action_button_group_box")
        self.action_button_group_box.setMinimumSize(QSize(200, 0))
        self.action_button_group_box.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.action_button_group_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.remove_add_character_limit_btn = QPushButton(self.action_button_group_box)
        self.remove_add_character_limit_btn.setObjectName(u"remove_add_character_limit_btn")

        self.verticalLayout_2.addWidget(self.remove_add_character_limit_btn)

        self.reset_dungeon_count_btn = QPushButton(self.action_button_group_box)
        self.reset_dungeon_count_btn.setObjectName(u"reset_dungeon_count_btn")

        self.verticalLayout_2.addWidget(self.reset_dungeon_count_btn)

        self.remove_equipment_level_limit_btn = QPushButton(self.action_button_group_box)
        self.remove_equipment_level_limit_btn.setObjectName(u"remove_equipment_level_limit_btn")

        self.verticalLayout_2.addWidget(self.remove_equipment_level_limit_btn)

        self.enable_all_dungeon_difficulty_btn = QPushButton(self.action_button_group_box)
        self.enable_all_dungeon_difficulty_btn.setObjectName(u"enable_all_dungeon_difficulty_btn")

        self.verticalLayout_2.addWidget(self.enable_all_dungeon_difficulty_btn)

        self.enable_left_and_right_slot_btn = QPushButton(self.action_button_group_box)
        self.enable_left_and_right_slot_btn.setObjectName(u"enable_left_and_right_slot_btn")

        self.verticalLayout_2.addWidget(self.enable_left_and_right_slot_btn)

        self.max_expert_job_level_btn = QPushButton(self.action_button_group_box)
        self.max_expert_job_level_btn.setObjectName(u"max_expert_job_level_btn")

        self.verticalLayout_2.addWidget(self.max_expert_job_level_btn)

        self.another_holder = QWidget(self.action_button_group_box)
        self.another_holder.setObjectName(u"another_holder")

        self.verticalLayout_2.addWidget(self.another_holder)


        self.gridLayout.addWidget(self.action_button_group_box, 0, 4, 2, 1)

        self.charge_group_box = QGroupBox(character_info)
        self.charge_group_box.setObjectName(u"charge_group_box")
        self.charge_group_box.setMinimumSize(QSize(200, 0))
        self.charge_group_box.setMaximumSize(QSize(200, 16777215))
        self.formLayout_5 = QFormLayout(self.charge_group_box)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.charge_label = QLabel(self.charge_group_box)
        self.charge_label.setObjectName(u"charge_label")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.LabelRole, self.charge_label)

        self.charge_spin_box = QDoubleSpinBox(self.charge_group_box)
        self.charge_spin_box.setObjectName(u"charge_spin_box")
        self.charge_spin_box.setDecimals(0)
        self.charge_spin_box.setMaximum(4294967295.000000000000000)

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.FieldRole, self.charge_spin_box)

        self.btn_group = QWidget(self.charge_group_box)
        self.btn_group.setObjectName(u"btn_group")
        self.btn_group.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(self.btn_group)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.charge_btn = QPushButton(self.btn_group)
        self.charge_btn.setObjectName(u"charge_btn")

        self.verticalLayout.addWidget(self.charge_btn)

        self.clear_btn = QPushButton(self.btn_group)
        self.clear_btn.setObjectName(u"clear_btn")

        self.verticalLayout.addWidget(self.clear_btn)


        self.formLayout_5.setWidget(8, QFormLayout.ItemRole.SpanningRole, self.btn_group)

        self.charge_type_label = QLabel(self.charge_group_box)
        self.charge_type_label.setObjectName(u"charge_type_label")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.charge_type_label)

        self.charge_type_combox = QComboBox(self.charge_group_box)
        self.charge_type_combox.setObjectName(u"charge_type_combox")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.charge_type_combox)


        self.gridLayout.addWidget(self.charge_group_box, 1, 3, 1, 1)

        self.pvp_group_box = QGroupBox(character_info)
        self.pvp_group_box.setObjectName(u"pvp_group_box")
        sizePolicy.setHeightForWidth(self.pvp_group_box.sizePolicy().hasHeightForWidth())
        self.pvp_group_box.setSizePolicy(sizePolicy)
        self.pvp_group_box.setMinimumSize(QSize(200, 0))
        self.pvp_group_box.setMaximumSize(QSize(200, 16777215))
        self.formLayout_2 = QFormLayout(self.pvp_group_box)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(8, 8, 8, -1)
        self.grade_label = QLabel(self.pvp_group_box)
        self.grade_label.setObjectName(u"grade_label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.grade_label)

        self.grade_combox = QComboBox(self.pvp_group_box)
        self.grade_combox.setObjectName(u"grade_combox")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grade_combox)

        self.win_label = QLabel(self.pvp_group_box)
        self.win_label.setObjectName(u"win_label")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.win_label)

        self.win_spinbox = QSpinBox(self.pvp_group_box)
        self.win_spinbox.setObjectName(u"win_spinbox")
        self.win_spinbox.setMaximum(2147483647)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.win_spinbox)

        self.win_point_label = QLabel(self.pvp_group_box)
        self.win_point_label.setObjectName(u"win_point_label")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.win_point_label)

        self.win_point_spin_box = QSpinBox(self.pvp_group_box)
        self.win_point_spin_box.setObjectName(u"win_point_spin_box")
        self.win_point_spin_box.setMaximum(2147483647)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.win_point_spin_box)

        self.save_pvp_btn = QPushButton(self.pvp_group_box)
        self.save_pvp_btn.setObjectName(u"save_pvp_btn")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.save_pvp_btn)


        self.gridLayout.addWidget(self.pvp_group_box, 0, 1, 1, 1)

        self.placeholder = QWidget(character_info)
        self.placeholder.setObjectName(u"placeholder")

        self.gridLayout.addWidget(self.placeholder, 0, 5, 1, 1)


        self.retranslateUi(character_info)

        QMetaObject.connectSlotsByName(character_info)
    # setupUi

    def retranslateUi(self, character_info):
        character_info.setWindowTitle(QCoreApplication.translate("character_info", u"Form", None))
        self.points_group_box.setTitle(QCoreApplication.translate("character_info", u"\u70b9\u6570\u4fe1\u606f", None))
        self.cash_cera_label.setText(QCoreApplication.translate("character_info", u"\u70b9\u5238", None))
        self.cash_cera_point_label.setText(QCoreApplication.translate("character_info", u"\u4ee3\u5e01", None))
        self.sp_label.setText(QCoreApplication.translate("character_info", u"SP", None))
        self.qp_label.setText(QCoreApplication.translate("character_info", u"QP", None))
        self.tp_label.setText(QCoreApplication.translate("character_info", u"TP", None))
        self.coin_group_box.setTitle(QCoreApplication.translate("character_info", u"\u91d1\u5e01 \u590d\u6d3b\u5e01", None))
        self.cargo_coin_label.setText(QCoreApplication.translate("character_info", u"\u91d1\u5e93\u91d1\u5e01", None))
        self.backpack_coin_label.setText(QCoreApplication.translate("character_info", u"\u80cc\u5305\u91d1\u5e01", None))
        self.pay_coin_label.setText(QCoreApplication.translate("character_info", u"\u590d\u6d3b\u5e01", None))
        self.save_coin_btn.setText(QCoreApplication.translate("character_info", u"Save", None))
        self.character_info_group_box.setTitle(QCoreApplication.translate("character_info", u"\u89d2\u8272\u4fe1\u606f", None))
        self.name_label.setText(QCoreApplication.translate("character_info", u"\u540d\u79f0", None))
        self.level_label.setText(QCoreApplication.translate("character_info", u"\u7b49\u7ea7", None))
        self.role_label.setText(QCoreApplication.translate("character_info", u"\u89d2\u8272", None))
        self.job_label.setText(QCoreApplication.translate("character_info", u"\u804c\u4e1a", None))
        self.wake_label.setText(QCoreApplication.translate("character_info", u"\u89c9\u9192", None))
        self.expert_label.setText(QCoreApplication.translate("character_info", u"\u526f\u804c\u4e1a", None))
        self.save_character_info_btn.setText(QCoreApplication.translate("character_info", u"Save", None))
        self.action_button_group_box.setTitle(QCoreApplication.translate("character_info", u"\u5176\u4ed6\u529f\u80fd", None))
        self.remove_add_character_limit_btn.setText(QCoreApplication.translate("character_info", u"\u89e3\u9664\u5efa\u53f7\u9650\u5236", None))
        self.reset_dungeon_count_btn.setText(QCoreApplication.translate("character_info", u"\u91cd\u7f6e\u526f\u672c\u6b21\u6570", None))
        self.remove_equipment_level_limit_btn.setText(QCoreApplication.translate("character_info", u"\u53d6\u6d88\u88c5\u5907\u7b49\u7ea7\u9650\u5236", None))
        self.enable_all_dungeon_difficulty_btn.setText(QCoreApplication.translate("character_info", u"\u5f00\u542f\u5168\u56fe\u96be\u5ea6", None))
        self.enable_left_and_right_slot_btn.setText(QCoreApplication.translate("character_info", u"\u5f00\u542f\u5de6\u53f3\u69fd", None))
        self.max_expert_job_level_btn.setText(QCoreApplication.translate("character_info", u"\u8bbe\u7f6e\u526f\u804c\u4e1a\u6ee1\u7ea7", None))
        self.charge_group_box.setTitle(QCoreApplication.translate("character_info", u"\u5145\u503c", None))
        self.charge_label.setText(QCoreApplication.translate("character_info", u"\u5145\u503c\u91cf", None))
        self.charge_btn.setText(QCoreApplication.translate("character_info", u"\u5145\u503c", None))
        self.clear_btn.setText(QCoreApplication.translate("character_info", u"\u6e05\u96f6", None))
        self.charge_type_label.setText(QCoreApplication.translate("character_info", u"\u5145\u503c\u7c7b\u578b", None))
        self.pvp_group_box.setTitle(QCoreApplication.translate("character_info", u"PVP", None))
        self.grade_label.setText(QCoreApplication.translate("character_info", u"\u6bb5\u4f4d", None))
        self.win_label.setText(QCoreApplication.translate("character_info", u"\u80dc\u573a", None))
        self.win_point_label.setText(QCoreApplication.translate("character_info", u"\u80dc\u70b9", None))
        self.save_pvp_btn.setText(QCoreApplication.translate("character_info", u"Save", None))
    # retranslateUi

