from ui.components.equipment_search.equipment_search import render_as_html


def test_render_as_html():
    output = '/Users/evrins/workspace/python/dnf_gm_tool/dump/equipment.html'
    data = {
        'display_attach_type': '封装',
        'display_equipment_type': '上衣',
        'display_rarity': '稀有',
        'display_usable_job': '全部职业',
        'durability': '40/40',
        'flavor': '',
        'name': '鳞岩胸甲',
        'name2': 'Carbollite Breastplate',
        'price': 6720.0,
        'required_level': 'Lv40以上可以使用',
        'rest': ['[激光炮]技能等级 +1', '套装名: 鳞岩重甲  套装'],
        'stat_property_1': ['物理防御力 +2160', '力量 +19', '体力 +17', '智力 +14'],
        'stat_property_2': [],
        'weight': '2.4kg',
    }
    with open(output, 'w') as f:
        f.write(render_as_html(data))
