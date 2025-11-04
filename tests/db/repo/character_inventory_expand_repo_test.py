from dnfpkgtool.db.repo.character_inventory_expand_repo import (
    CharacterInventoryExpandRepo,
)


def test_query_by_character_no():
    repo = CharacterInventoryExpandRepo()
    character_inventor = repo.query_by_character_no(2)
    print(character_inventor)
