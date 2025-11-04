from dnfpkgtool.db.repo.character_info_repo import CharacterInfoRepo


def test_query_all_characters():
    repo = CharacterInfoRepo()
    for character in repo.query_all_character_info_list():
        print(character.__dict__)
