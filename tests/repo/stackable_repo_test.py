from config import config
from dnfpkgtool.repo.stackable_repo import StackableRepo


def test_query():
    fp = config.get_stackable_parquet_file_path()
    stackable_repo = StackableRepo(str(fp))
    rs = stackable_repo.query('药', max_level=50)
    print(len(rs))


def test_query_by_id():
    fp = config.get_stackable_parquet_file_path()
    stackable_repo = StackableRepo(str(fp))
    res = stackable_repo.query_by_id(1)
    print()
    print(res)
