from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.event_1306_account_reward import Event1306AccountReward
from dnfpkgtool.db.repo.base_repo import BaseRepo


class Event1306AccountRewardRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_game_event')

    def query_character_no_by_m_id_list(self, m_id_list: List[int]) -> List[int]:
        with Session(self.get_engine()) as session:
            stmt = select(Event1306AccountReward.charac_no).where(
                Event1306AccountReward.m_id.in_(m_id_list)
            )
            return list(session.scalars(stmt).all())
