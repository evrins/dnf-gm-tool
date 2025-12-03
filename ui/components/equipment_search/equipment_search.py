import json
from typing import Dict, List

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
    QTimer,
)
from PySide6.QtWidgets import (
    QWidget,
)

from dnfpkgtool.db.entity.mail_form_item import MailItemType
from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.repo.equipment_repo import EquipmentRepo
from dnfpkgtool.repo.orb_repo import render_skills_text
from dnfpkgtool.repo.repo_manager import get_equipment_repo, get_skill_repo
from dnfpkgtool.repo.skill_repo import SkillRepo
from ui.components.equipment_search.equipment_search_ui import Ui_equipment_search
from ui.components.stackable_search.vars import (
    default_options,
    equipment_name_mapping,
    job_name_mapping,
    main_options,
    minor_options,
    patch_options,
    rarity_list,
)


class EquipmentTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = [
            'id',
            'name',
            'display_equipment_type',
            'display_usable_job',
            'minimum_level',
            'display_rarity',
        ]
        self._headers_display = ['ID', '名称', '装备类型', '可用职业', '等级', '稀有度']

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            key = self._headers[index.column()]
            return self._data[index.row()][key]
        elif role == Qt.ItemDataRole.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers_display[section]
        return None

    def flags(self, index) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class EquipmentSearch(QWidget, Ui_equipment_search):
    equipment_repo: EquipmentRepo
    skill_repo: SkillRepo

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.set_repo()

        gs.pvf_changed.connect(self.set_repo)

        self.name_line_edit.returnPressed.connect(self.do_search)
        self.main_combox.addItems(main_options)
        self.main_combox.currentTextChanged.connect(self.main_option_changed)

        self.minor_combox.addItems(default_options)
        self.minor_combox.setEnabled(False)
        self.minor_combox.currentTextChanged.connect(self.minor_option_changed)

        self.patch_combox.addItems(default_options)
        self.patch_combox.setEnabled(False)

        self.rarity_combox.addItem('---')
        self.rarity_combox.addItems(rarity_list)

        self.search_btn.clicked.connect(self.do_search)

        self.submit_btn.clicked.connect(self.submit_to_mail)

    def set_repo(self):
        self.equipment_repo = get_equipment_repo()
        self.skill_repo = get_skill_repo()

    def _adjust_table_columns(self):
        """Adjust table column widths to content."""
        self.result_table_view.resizeColumnsToContents()

    def adjust_size_to_content(self):
        """Public method to adjust table columns to content."""
        self._adjust_table_columns()

    def main_option_changed(self, text: str):
        next_minor_options = minor_options.get(text, default_options)
        enable_minor_option = next_minor_options != default_options

        self.minor_combox.clear()
        self.minor_combox.addItems(next_minor_options)
        self.minor_combox.setEnabled(enable_minor_option)

    def minor_option_changed(self, text: str):
        key = f'{self.main_combox.currentText()}/{text}'
        next_patch_options = patch_options.get(key, default_options)
        enable_patch_option = next_patch_options != default_options

        self.patch_combox.clear()
        self.patch_combox.addItems(next_patch_options)
        self.patch_combox.setEnabled(enable_patch_option)

    def do_search(self, s=None):
        name = self.name_line_edit.text().strip()
        main_option = self.main_combox.currentText()
        minor_option = self.minor_combox.currentText()
        patch_option = self.patch_combox.currentText()

        equipment_type_list = None
        usable_job = None
        item_group_name = None
        armor_type = None

        if main_option == '---':
            equipment_type_list = None
        elif main_option == '武器':
            equipment_type_list = ['[weapon]']
            usable_job = job_name_mapping[minor_option]
            item_group_name = equipment_name_mapping[patch_option]
        elif main_option == '防具':
            selected_equipment_type = equipment_name_mapping[patch_option]
            if selected_equipment_type is None:
                equipment_type_list = [
                    '[coat]',
                    '[waist]',
                    '[shoulder]',
                    '[shoes]',
                    '[pants]',
                ]
            else:
                equipment_type_list = [selected_equipment_type]
            armor_type = equipment_name_mapping[minor_option]
        elif main_option == '首饰':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = ['[amulet]', '[wrist]', '[ring]']
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '特殊装备':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = ['[support]', '[magic stone]']
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '装扮':
            selected_equipment_type = equipment_name_mapping[minor_option]
            if selected_equipment_type is None:
                equipment_type_list = [
                    '[aurora avatar]',
                    '[hair avatar]',
                    '[hat avatar]',
                    '[face avatar]',
                    '[breast avatar]',
                    '[coat avatar]',
                    '[skin avatar]',
                    '[waist avatar]',
                    '[pants avatar]',
                    '[shoes avatar]',
                ]
            else:
                equipment_type_list = [selected_equipment_type]
            usable_job = job_name_mapping[patch_option]
        elif main_option == '宠物':
            equipment_type_list = ['[creature]']
        elif main_option == '称号':
            equipment_type_list = ['[title name]']
        elif main_option == '宠物装备':
            equipment_type_list = [
                '[artifact blue]',
                '[artifact green]',
                '[artifact red]',
            ]
        elif main_option == '契约效果':
            equipment_type_list = ['']
        else:
            raise Exception(f'unknown main option: {main_option}')

        min_level = self.ranged_spinbox.min_level_spinbox.value()
        min_level = None if min_level == 0 else int(min_level)
        max_level = self.ranged_spinbox.max_level_spinbox.value()
        max_level = None if max_level == 0 else int(max_level)

        rarity = self.rarity_combox.currentText()
        rarity = None if rarity == '---' else rarity

        data = self.equipment_repo.query(
            name,
            equipment_type_list,
            usable_job,
            item_group_name,
            armor_type,
            min_level=min_level,
            max_level=max_level,
            rarity=rarity,
            limit=1024,
        )
        self.update_title(len(data))
        table_model = EquipmentTableModel(data)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(table_model)
        self.result_table_view.setModel(proxy_model)

        self.selection_model = self.result_table_view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)

        self.result_table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # Adjust table columns to content
        QTimer.singleShot(100, self._adjust_table_columns)

    def submit_to_mail(self):
        selected_indexes = self.result_table_view.selectedIndexes()
        if not selected_indexes:
            return
        row = selected_indexes[0].data(Qt.ItemDataRole.UserRole)
        mail_submit_item = MailSubmitItem(
            item_id=row['id'],
            item_name=row['name'],
            item_type=MailItemType.Equipment,
            endurance=row['durability'],
            sub_type=row['sub_type'],
        )

        equipment_type = row['equipment_type']
        if equipment_type in [
            '[aurora avatar]',
            '[hair avatar]',
            '[hat avatar]',
            '[face avatar]',
            '[breast avatar]',
            '[coat avatar]',
            '[skin avatar]',
            '[waist avatar]',
            '[pants avatar]',
            '[shoes avatar]',
        ]:
            mail_submit_item.item_type = MailItemType.Avatar
        elif equipment_type in ['[creature]']:
            mail_submit_item.item_type = MailItemType.Creature

        gs.submit_mail_form.emit(mail_submit_item)

    def on_selection_changed(self, selected, deselected):
        indent = ' ' * 4
        rows = self.selection_model.selectedRows()
        if not rows:
            return
        row = rows[0].data(Qt.ItemDataRole.UserRole)
        detail = self.render_detail(row)
        self.detail_text_edit.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.detail_text_edit.setText(detail)

    def update_title(self, n_result: int):
        title = '结果'
        if n_result > 1000:
            title = f'找到 {title} 1000+ 条记录'
        elif n_result > 0:
            title = f'找到 {n_result} 条记录'
        self.search_results.setTitle(title)

    def render_detail(self, equipment: Dict) -> str:
        detail = [
            f"名称: {equipment['name']}",
            f"名称2: {equipment['name2']}",
            f"等级: {equipment['minimum_level']}",
            f"稀有度: {equipment['display_rarity']}",
            f"类型: {equipment['display_equipment_type']}",
        ]

        detail.extend(render_stat_property(self.skill_repo, equipment))

        if explain := equipment['basic_explain']:
            detail.append(f'说明: {explain.replace('%%', '%')}')

        if set_name := equipment['set_name']:
            detail.append(f'套装名: {set_name}')

        master_set_item_id = equipment['set_item_master']
        if master_set_item_id != 0:
            master_set_item = self.equipment_repo.query_by_id(master_set_item_id)
        else:
            master_set_item = equipment

        if fullset_detail_explain := master_set_item['set_ability']['fullset_detail_explain']:
            detail.append(f'套装效果: {fullset_detail_explain.replace('%%', '%')}')
        elif fullset_basic_explain := master_set_item['set_ability']['fullset_basic_explain']:
            detail.append(f'套装效果: {fullset_basic_explain.replace('%%', '%')}')

        if skill_level_up_list := master_set_item['skill_level_up']:
            detail.append('技能增强')
            for it in skill_level_up_list:
                job = it['role'].replace('[', '').replace(']', '').replace(' ', '').lower()
                skill = self.skill_repo.query_by_job_and_id_of_job(job, it['skill_id'])
                if skill:
                    detail.append(f'    {skill["name"]} +{it["level_up"]}')

        if flavor_text := equipment['flavor_text']:
            detail.append(f'\n{flavor_text}')

        return '\n'.join(detail)


def render_stat_property(skill_repo: SkillRepo, d: Dict) -> List[str]:
    valid_keys = {
        'equipment_physical_attack': '物理攻击力',
        'equipment_magical_attack': '魔法攻击力',
        'separate_attack': '独立攻击力',
        'equipment_physical_defense': '物理防御力',
        'equipment_magical_defense': '魔法防御力',

        'physical_attack': '力量',
        'physical_defense': '体力',
        'magical_attack': '智力',
        'magical_defense': '精神',
        'hp_max': 'HP 最大值',
        'mp_max': 'MP 最大值',
        'hp_regen_speed': 'HP 回复速度',
        'hp_regen_speed_rate': 'HP 回复速度',
        'mp_regen_speed': 'MP 回复速度',
        'mp_regen_speed_rate': 'MP 回复速度',
        'move_speed': '移动速度',
        'attack_speed': '攻击速度',
        'cast_speed': '释放速度',

        'physical_critical_hit': '物理暴击率',
        'magical_critical_hit': '魔法暴击率',

        'stuck': '命中率',
        'rigidity': '僵直',
        'hit_recovery': '硬直',
        'all_elemental_attack': '所有属性攻击',
        'all_elemental_resistance': '所有属性抗性',
        'stuck_resistance': '回避率',
        'stun_resistance': '眩晕抗性',
        'piercing_resistance': '穿刺抗性',
        'freeze_resistance': '冰冻抗性',
        'confuse_resistance': '混乱抗性',
        'poison_resistance': '中毒抗性',
        'stone_resistance': '石化抗性',
        'blind_resistance': '致盲抗性',
        'curse_resistance': '诅咒抗性',
        'bleeding_resistance': '出血抗性',
        'lightning_resistance': '感电抗性',
        'burn_resistance': '灼烧抗性',
        'sleep_resistance': '睡眠抗性',
        'slow_resistance': '减速抗性',
        'hold_resistance': '束缚抗性',

        'dark_attack': '暗属性强化',
        'light_attack': '光属性强化',
        'fire_attack': '火属性强化',
        'water_attack': '冰属性强化',

        'dark_resistance': '暗属性抗性',
        'light_resistance': '光属性抗性',
        'fire_resistance': '火属性抗性',
        'water_resistance': '冰属性抗性',

        'all_activestatus_resistance': '所有异常状态抗性',
        'room_list_move_speed_rate': '地图移动速度',
        'jump_power': '跳跃力',


        'anti_evil': '抗魔值',

        'elemental_property': '属性攻击',

        'creature_magical_attack': '宠物魔法攻击力',
        'creature_physical_attack': '宠物物理攻击力',
        'creature_skill_charge_time_rate': '宠物蓄力时间',

        'hp_max_rate': 'HP 最大值',
        'mp_max_rate': 'MP 最大值',

        'lift_up': 'lift_up',

        'inventory_limit': '负重'
    }

    res = []

    for k, v in valid_keys.items():
        vv = d.get(k)
        if not vv:
            continue

        if k == 'elemental_property':
            if vv == '[light element]':
                res.append('光属性攻击')
            elif vv == '[fire element]':
                res.append('火属性攻击')
            elif vv == '[water element]':
                res.append('冰属性攻击')
            elif vv == '[dark element]':
                res.append('暗属性攻击')
            else:
                res.append('未知属性')
        elif k == 'stuck':
            if abs(vv) < 1:
                res.append(f'{v} {vv:+.1}%')
            else:
                res.append(f'{v} {vv:+}%')
        elif k in ['attack_speed', 'move_speed', 'cast_speed']:
            vv = vv / 10
            res.append(f'{v} {vv:+.1f}%')
        elif k in ['physical_critical_hit', 'magical_critical_hit',
                   'hp_max_rate', 'mp_max_rate',
                   'hp_regen_speed_rate', 'mp_regen_speed_rate']:
            res.append(f'{v} {vv:+}%')
        elif k == 'skill_level_up':
            res.extend(render_skills_text(skill_repo, v))
        elif k == 'all_skill_item_container':
            if not v['all_skill_item']['item_grow_type']:
                continue

            lower = v['all_skill_item']['skill_apply_condition']['lower_bound_level']
            upper = v['all_skill_item']['skill_apply_condition']['upper_bound_level']
            level = v['all_skill_item']['skill_apply_condition']['value']
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        elif k == 'all_skill_item':
            if not v['skill_apply_condition']['item_grow_type']:
                continue

            lower = v['skill_apply_condition']['lower_bound_level']
            upper = v['skill_apply_condition']['upper_bound_level']
            level = v['skill_apply_condition']['value']
            res.append(f'{lower}-{upper} 主动技能等级 +{level}')
        else:
            res.append(f'{v} {vv:+}')

    return res