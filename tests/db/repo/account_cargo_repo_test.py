from dnfpkgtool.db.repo.account_cargo_repo import AccountCargoRepo


def test_query_by_m_id():
    repo = AccountCargoRepo()
    item = repo.query_by_m_id(18000000)
    print(item.__dict__)
