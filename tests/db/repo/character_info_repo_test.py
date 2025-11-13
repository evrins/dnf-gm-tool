from dnfpkgtool.db.repo.character_info_repo import CharacterInfoRepo
from util import utf8_to_cp1252


def test_query_all_characters():
    repo = CharacterInfoRepo()
    for character in repo.query_all_character_info_list():
        print(character.__dict__)


def test_apply_map_function_decorator():
    from dnfpkgtool.db.repo.character_info_repo import apply_map_function, fix_character_name_encoding
    from dnfpkgtool.db.model.character_info import CharacterInfo
    
    # Create a mock function that returns a list of CharacterInfo
    @apply_map_function(fix_character_name_encoding)
    def mock_query():
        # Simulate a character with garbled Chinese name
        char = CharacterInfo()
        char.character_no = 1
        char.character_name = utf8_to_cp1252('你好世界')  # Simulated mojibake
        char.lev = 100
        char.job = 1
        char.grow_type = 1
        char.delete_flag = 0
        char.expert_job = 0
        char.m_id = 1
        return [char]
    
    # Execute the decorated function
    result = mock_query()
    
    print(f"Fixed character name: {result[0].character_name}")
    
    # Verify the name was fixed
    assert result[0].character_name == '你好世界', f"Expected '你好世界', got '{result[0].character_name}'"
    print("✓ Map function decorator test passed!")
