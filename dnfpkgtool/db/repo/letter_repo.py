from sqlalchemy.orm import Session

from dnfpkgtool.db.model.letter import Letter
from dnfpkgtool.db.repo.base_repo import BaseRepo


class LetterRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def add(self, letter: Letter) -> Letter:
        with Session(self.get_engine()) as session:
            session.add(letter)
            session.commit()
            session.refresh(letter)  # Refresh to get the auto-generated ID
            return letter


def get_letter_repo() -> LetterRepo:
    return LetterRepo()
