from dnf_db.repo import AccountsRepo


def test_query_all():
    repo = AccountsRepo()
    for it in repo.query_all():
        print(it.__dict__)
