from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.skill import Skill
from dnfpkgtool.db.repo.base_repo import BaseRepo


class SkillRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain_2nd')

    def query_by_character_no(self, character_no: int) -> Skill:
        with Session(self.get_engine()) as session:
            stmt = select(Skill).where(Skill.charac_no == character_no).limit(1)
            return session.scalars(stmt).first()

    def charge(self, it: Skill):
        with Session(self.get_engine()) as session:
            stmt = (
                update(Skill)
                .where(Skill.charac_no == it.charac_no)
                .values(
                    remain_sp=Skill.remain_sp + it.remain_sp,
                    remain_sp_2nd=Skill.remain_sp_2nd + it.remain_sp_2nd,
                    remain_sfp_1st=Skill.remain_sfp_1st + it.remain_sfp_1st,
                    remain_sfp_2nd=Skill.remain_sfp_2nd + it.remain_sfp_2nd,
                )
            )
            session.execute(stmt)
            session.commit()

    def clear_sp_by_character_no(self, character_no: int):
        with Session(self.get_engine()) as session:
            stmt = (
                update(Skill)
                .where(Skill.charac_no == character_no)
                .values(
                    remain_sp=0,
                    remain_sp_2nd=0,
                )
            )
            session.execute(stmt)
            session.commit()

    def clear_tp_by_character_no(self, character_no: int):
        with Session(self.get_engine()) as session:
            stmt = (
                update(Skill)
                .where(Skill.charac_no == character_no)
                .values(
                    remain_sfp_1st=0,
                    remain_sfp_2nd=0,
                )
            )
            session.execute(stmt)
            session.commit()


def get_skill_repo() -> SkillRepo:
    return SkillRepo()
