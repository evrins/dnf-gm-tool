from dnfpkgtool.db.repo.inventory_repo import InventoryRepo


def test_query_by_character_no():
    repo = InventoryRepo()
    inventory = repo.query_by_character_no(2)
    print(inventory)
