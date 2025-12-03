from pydantic import BaseModel

from dnfpkgtool.pvf.entity.skill_apply_condition import SkillApplyCondition


class AllSkillItem(BaseModel):
    item_grow_type: str = ''
    skill_phase: str = ''
    skill_apply_condition: SkillApplyCondition | None = None
