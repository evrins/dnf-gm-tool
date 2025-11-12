#!/usr/bin/env python3
"""
Startup validation script for DNF GM Tool
Checks database connectivity and data file availability
"""

import sys

from loguru import logger

from config.config import check_mysql_config, get_config, get_db_config
from dnfpkgtool.repo.repo_manager import get_magic_seal_repo, get_orb_repo, get_skill_repo, get_stackable_repo


def check_database() -> bool:
    """Check database connectivity"""
    try:
        db_config = get_db_config()
        result = check_mysql_config(
            db_config.host, db_config.port, db_config.username, db_config.password
        )
        if result:
            logger.info('✅ Database connection: OK')
        else:
            logger.warning('❌ Database connection: FAILED')
        return result
    except Exception as e:
        logger.error(f'❌ Database connection error: {e}')
        return False


def check_parquet_files() -> bool:
    """Check if parquet data files are available"""
    try:
        config = get_config()
        if not config.have_valid_pvf():
            logger.warning('❌ PVF data: No valid PVF hash configured')
            return False

        # Test all repositories
        from dnfpkgtool.repo.repo_manager import get_equipment_repo

        repos_to_test = [
            ('Stackable', get_stackable_repo),
            ('Equipment', get_equipment_repo),
            ('Skill', get_skill_repo),
            ('Orb', get_orb_repo),
            ('Magic Seal', get_magic_seal_repo),
        ]

        all_available = True
        for repo_name, repo_getter in repos_to_test:
            try:
                repo = repo_getter()
                if repo.is_available():
                    logger.info(f'✅ {repo_name} data: OK')
                else:
                    logger.warning(f'❌ {repo_name} data: NOT AVAILABLE')
                    all_available = False
            except Exception as e:
                logger.error(f'❌ {repo_name} data error: {e}')
                all_available = False

        if all_available:
            logger.info('✅ All parquet data files: OK')
        else:
            logger.warning('❌ Some parquet data files: NOT AVAILABLE')

        return all_available
    except Exception as e:
        logger.error(f'❌ Parquet data files error: {e}')
        return False


def main():
    """Run startup checks"""
    logger.info('Running DNF GM Tool startup checks...')

    db_ok = check_database()
    data_ok = check_parquet_files()

    if db_ok and data_ok:
        logger.info('🎉 All systems ready! Application should start without issues.')
        return 0
    else:
        logger.warning(
            '⚠️  Some systems are not ready. Application will start with limited functionality.'
        )
        if not db_ok:
            logger.info(
                '💡 To fix database: Configure database settings in the Settings tab'
            )
        if not data_ok:
            logger.info('💡 To fix data files: Process PVF files in the Settings tab')
        return 1


if __name__ == '__main__':
    sys.exit(main())
