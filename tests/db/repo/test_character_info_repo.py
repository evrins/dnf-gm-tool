from config import config
from dnf_db.model.character_info import CharacterInfo
from dnf_db.repo.character_info_repo import CharacterInfoRepo


def test_update_character_info():
    config.load()
    ci = CharacterInfo(
        m_id=18000000,
        character_no=11,
        character_name='你好世界22',
        lev=70,
        job=2,
        grow_type=18,
        delete_flag=0,
        expert_job=0,
    )

    repo = CharacterInfoRepo()
    repo.update_character_info(ci)
