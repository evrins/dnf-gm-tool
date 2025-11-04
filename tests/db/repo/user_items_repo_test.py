from dnfpkgtool.db.repo.user_items_repo import UserItemsRepo


def test_query_user_items_repo() -> None:
    repo = UserItemsRepo()
    it = repo.query_by_id(61)
    print(it)
