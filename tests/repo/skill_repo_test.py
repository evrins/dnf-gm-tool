from config import config
from pvf.repo.skill_repo import SkillRepo


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
