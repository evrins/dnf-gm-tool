from dnfpkgtool.db.repo.event_1306_account_reward_repo import Event1306AccountRewardRepo


def test_query_character_no_by_m_id_list():
    repo = Event1306AccountRewardRepo()
    m_id_list = [18000000]
    for char_no in repo.query_character_no_by_m_id_list(m_id_list):
        print(char_no)
