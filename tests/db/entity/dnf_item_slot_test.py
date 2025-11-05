from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot


def test_default_to_bytes():
    item = DnfItemSlot.default()
    print(item.to_bytes())
