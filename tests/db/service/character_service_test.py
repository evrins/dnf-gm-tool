from config import config
from dnfpkgtool.db.service.character_service import get_character_service


def test_get_current_money():
    config.load()
    cs = get_character_service()
