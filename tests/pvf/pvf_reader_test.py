import json
import os
from pathlib import Path

from dnfpkgtool.pvf.pvf_reader import PVFReader

base_dir = Path(__file__).parent / 'dump'

os.makedirs(base_dir, exist_ok=True)


def save_obj_2_file(obj, filename):
    with open(base_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def test_pvf_reader():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    st = reader.string_table

    all_strings = []
    for i in range(2 * st.length):
        all_strings.append(st[i])

    all_strings.sort()
    with open(base_dir / 'string_table.txt', 'w') as f:
        f.writelines(all_strings)


def test_get_quest_dict():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    quest_dict = reader.get_quest_dict()
    save_obj_2_file(quest_dict, 'quest_dict.json')


def test_get_dungeon_dict():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    dungeon_dict = reader.get_dungeon_dict()
    save_obj_2_file(dungeon_dict, 'dungeon_dict.json')


def test_get_magic_seal_dict():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    magic_seal_dict = reader.get_magic_seal_dict()
    save_obj_2_file(magic_seal_dict, 'magic_seal_dict.json')


def test_get_magic_seal_as_list():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    magic_seal_list = reader.read_file_as_list(
        'etc/randomoption/randomizedoptionoverall2.etc'
    )
    save_obj_2_file(magic_seal_list, 'magic_seal_list.json')
    magic_seal_dict = reader.read_file_as_dict(
        'etc/randomoption/randomizedoptionoverall2.etc'
    )
    save_obj_2_file(magic_seal_dict, 'magic_seal_dict.json')


def test_get_job_dict():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    job_dict = reader.get_job_dict()
    save_obj_2_file(job_dict, 'job_dict.json')


def test_get_exp_table():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    exp_table = reader.get_exp_table()
    save_obj_2_file(exp_table, 'exp_table.json')


def test_get_stackable_dict():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    stackable_dict = reader.get_stackable_dict()
    save_obj_2_file(stackable_dict, 'stackable_dict.json')


def test_get_avatar_hidden_fixed():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    avatar_hidden_dict = reader.get_avatar_hidden_fixed()
    save_obj_2_file(avatar_hidden_dict, 'stackable_dict.json')


def test_get_equipment():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    equipment_dict = reader.get_equipment_dict()
    save_obj_2_file(equipment_dict, 'equipment_dict.json')


def test_get_skill_list():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    skill_dict = reader.get_skill_list()
    save_obj_2_file(skill_dict, 'skill_list.json')


def test_read_lst_file():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    equipment_list = reader.load_lst_file('equipment/equipment.lst')
    save_obj_2_file(equipment_list.table_dict, 'equipment_list.json')


def read_single_equipment(equipment_id):
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    equipments = reader.load_lst_file('equipment/equipment.lst')
    sub_path = 'equipment/' + equipments.table_dict[equipment_id]
    equipment_as_list = reader.read_file_as_list(sub_path)
    save_obj_2_file(equipment_as_list, f'equipment_{equipment_id}.list.json')
    equipment_as_dict = reader.read_file_as_dict(sub_path)
    save_obj_2_file(equipment_as_dict, f'equipment_{equipment_id}.dict.json')


def test_read_single_equipment_29015():
    equipment_id = 29015
    read_single_equipment(equipment_id)


def test_read_single_equipment_11253():
    equipment_id = 11253
    read_single_equipment(equipment_id)


def test_read_single_equipment_19319():
    equipment_id = 19319
    read_single_equipment(equipment_id)
