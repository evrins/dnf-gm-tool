from sqlalchemy import update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_blood_dungeon_reward import (
    CharacterBloodDungeonReward,
)
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterBloodDungeonRewardRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def update(self, it: CharacterBloodDungeonReward):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterBloodDungeonReward)
                .where(CharacterBloodDungeonReward.character_no == it.character_no)
                .values(
                    enter_count=it.enter_count,
                )
            )
            session.execute(stmt)
            session.commit()


def get_character_blood_dungeon_reward_repo() -> CharacterBloodDungeonRewardRepo:
    return CharacterBloodDungeonRewardRepo()
