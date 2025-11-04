from dnfpkgtool.db.service.account_service import AccountService


def test_query_all_online_character_list() -> None:
    account_service = AccountService()
    character_list = account_service.get_online_character_list()
    for it in character_list:
        print(it.__dict__)


def test_query_all_character_account_list() -> None:
    account_service = AccountService()
    character_list = account_service.get_all_character_list()
    for it in character_list:
        print(it.__dict__)
