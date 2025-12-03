from dnfpkgtool.pvf.entity.stat_property import StatProperty


class SetAbility(StatProperty):
    set_name: int | None = None
    fullset_basic_explain: str | None = None
    fullset_detail_explain: str | None = None
