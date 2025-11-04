import pymysql
from loguru import logger


def check_mysql_config(
    host: str,
    port: int,
    user: str,
    password: str,
) -> bool:
    conn = None
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database='d_taiwan',
            connect_timeout=5,
        )

        conn.ping(True)

    except pymysql.Error as err:
        logger.error(f'error connecting to database: {err}')
        return False
    finally:
        if conn and conn.open:
            conn.close()
            logger.info('database connection closed')
            return True

    return False
