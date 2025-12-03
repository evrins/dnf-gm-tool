from itertools import chain

import polars as pl

from dnfpkgtool.repo.orb_repo import (
    build_orb_repo_parquet,
    enchant_key_mapping,
    orb_category_order,
)
from dnfpkgtool.repo.repo_manager import (
    get_orb_repo,
)
from dnfpkgtool.repo.skill_repo import SkillRepo
from dnfpkgtool.repo.stackable_repo import StackableRepo


def test_build_orb_repo_parquet():
    stackable_repo = StackableRepo('/Users/evrins/workspace/python/dnf_gm_tool/dump/stackables.parquet')
    skill_repo = SkillRepo('/Users/evrins/workspace/python/dnf_gm_tool/dump/skills.parquet')
    build_orb_repo_parquet(
        stackable_repo, skill_repo, '/Users/evrins/workspace/python/dnf_gm_tool/dump/orbs.parquet'
    )


def test_build_orb_options():
    d = {v: (i + 1) * 10 for i, v in enumerate(enchant_key_mapping.values())}
    print(d)

    orb_repo = get_orb_repo()
    df = orb_repo.df
    parts = df.select('apply_parts').to_series().to_list()

    parts = list(set(chain.from_iterable(parts)))
    options = {}
    for p in parts:
        category_list = (
            df.filter(pl.col('apply_parts').list.contains(p))
            .select(pl.col('display_enchant_category'))
            .to_series()
            .to_list()
        )
        category_list = list(set(chain.from_iterable(category_list)))
        category_list = sorted(category_list, key=lambda x: orb_category_order[x])
        options[p] = category_list

    print(options)
