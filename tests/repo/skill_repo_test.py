from config import config
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.skill_repo import SkillRepo, build_skill_repo_parquet


def test_build_skill_repo_parquet():
    pvf_path = '/Users/evrins/workspace/python/DNF_pvf_python/Script.pvf'
    reader = PVFReader(pvf_path)
    skill_list = reader.get_skill_list()
    build_skill_repo_parquet(skill_list, config.get_skill_parquet_file_path())


def test_query():
    fp = config.get_skill_parquet_file_path()
    skill_repo = SkillRepo(str(fp))
    rs = skill_repo.query('药')
    print(len(rs))


def test_query_by_job_and_id_of_job():
    fp = config.get_skill_parquet_file_path()
    skill_repo = SkillRepo(str(fp))
    rs = skill_repo.query_by_job_and_id_of_job('swordman', 2)
    print(rs)
