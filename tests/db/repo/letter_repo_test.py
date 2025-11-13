from datetime import datetime

from dnfpkgtool.db.model.letter import Letter
from dnfpkgtool.db.repo.letter_repo import LetterRepo


def test_add():
    repo = LetterRepo()
    letter = Letter(
        character_no=8,
        send_character_no=0,
        send_character_name='背包编辑工具'.encode('utf-8').decode(
            'latin1', errors='replace'
        ),
        letter_text='欢迎使用GM功能，有运行错误请提交issue至GitHub'.encode(
            'utf-8'
        ).decode('latin1', errors='replace'),
        reg_date=datetime.now(),
        stat=1,
    )

    # letter_id should be None before adding (will be auto-generated)
    assert letter.letter_id is None

    # Add the letter to the database
    letter = repo.add(letter)

    # letter_id should now be auto-generated and not None
    assert letter.letter_id is not None
    assert isinstance(letter.letter_id, int)
    assert letter.letter_id > 0

    print(f'Generated letter_id: {letter.letter_id}')


def test_handle_chinese():
    """Test that Chinese characters are properly handled in the database."""
    repo = LetterRepo()
    
    # Test data with Chinese characters
    test_name = '测试角色名'
    test_text = '这是一条测试消息，包含中文字符：你好世界！'
    
    letter = Letter(
        character_no=999,
        send_character_no=0,
        send_character_name=test_name,
        letter_text=test_text,
        reg_date=datetime.now(),
        stat=1,
    )
    
    # Add the letter to the database
    added_letter = repo.add(letter)
    
    # Verify the Chinese characters are preserved correctly
    assert added_letter.send_character_name == test_name
    assert added_letter.letter_text == test_text
    assert added_letter.letter_id is not None
    
    print(f'Chinese character test passed. Letter ID: {added_letter.letter_id}')
    print(f'Name: {added_letter.send_character_name}')
    print(f'Text: {added_letter.letter_text}')
