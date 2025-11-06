from dnfpkgtool.db.service.quest_service import QuestService


def test_get_current_character_quest():
    quest_service = QuestService()
    quest = quest_service.get_current_character_quest()
    print(quest)
