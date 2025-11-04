from dnfpkgtool.db.repo.login_account_3_repo import LoginAccount3Repo


def test_query_logged_account_m_id():
    repo = LoginAccount3Repo()
    for mid in repo.query_logged_account_m_id():
        print(mid)
