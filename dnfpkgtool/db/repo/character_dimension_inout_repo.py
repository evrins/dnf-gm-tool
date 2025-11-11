from sqlalchemy import update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_dimension_inout import CharacterDimensionInout
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterDimensionInoutRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def update(self, it: CharacterDimensionInout):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterDimensionInout)
                .where(CharacterDimensionInout.character_no == it.character_no)
                .values(
                    dungeon1=it.dungeon1,
                    dungeon2=it.dungeon2,
                    dungeon3=it.dungeon3,
                    dungeon4=it.dungeon4,
                    dungeon5=it.dungeon5,
                    dungeon6=it.dungeon6,
                    dungeon7=it.dungeon7,
                    dungeon8=it.dungeon8,
                    dungeon9=it.dungeon9,
                    dungeon10=it.dungeon10,
                )
            )
            session.execute(stmt)
            session.commit()


def get_character_dimension_inout_repo() -> CharacterDimensionInoutRepo:
    return CharacterDimensionInoutRepo()
