from pathlib import Path

from dnfpkgtool.pvf.pvf_header import parse_pvf_header
from tests.pvf.pvf_reader_test import save_obj_2_file

base_dir = Path(__file__).parent


def test_parse_pvf_header():
    fp = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    with open(fp, 'rb') as f:
        header = parse_pvf_header(f)
        header.leaf_dict = dict(sorted(header.leaf_dict.items()))
        leaf_dict = {}
        for k, v in header.leaf_dict.items():
            leaf_dict[k] = v.model_dump()
        save_obj_2_file(leaf_dict, 'header.json')


def test_filter_by_prefix():
    fp = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    prefix = 'equipment/character/partset/'
    with open(fp, 'rb') as f:
        header = parse_pvf_header(f)
        header.leaf_dict = dict(sorted(header.leaf_dict.items()))
        leaf_dict = {}
        count = 0
        for k, v in header.leaf_dict.items():
            if not k.startswith(prefix):
                continue
            leaf_dict[k] = v.model_dump()
            count += 1
            print(f'{count} : {k}')


def test_filter_by_suffix():
    fp = '/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf'
    suffix = '.lst'
    with open(fp, 'rb') as f:
        header = parse_pvf_header(f)
        header.leaf_dict = dict(sorted(header.leaf_dict.items()))
        leaf_dict = {}
        count = 0
        for k, v in header.leaf_dict.items():
            if not k.endswith(suffix):
                continue
            leaf_dict[k] = v.model_dump()
            count += 1
            print(f'{count} : {k}')
