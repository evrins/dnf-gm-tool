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
