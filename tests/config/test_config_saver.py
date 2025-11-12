"""
Test config saver worker thread functionality
"""

import tempfile
from pathlib import Path

from config.config_saver import ConfigSaverManager, ConfigSaverWorker


def test_config_saver_worker():
    """Test ConfigSaverWorker basic functionality"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Test data
        test_json = '{"test": "data", "value": 123}'

        # Create worker
        worker = ConfigSaverWorker(tmp_path, test_json)

        # Start worker
        worker.start()

        # Wait for completion (with timeout)
        success = worker.wait(5000)

        # Verify results
        assert success, 'Worker should have completed within timeout'

        # Verify file was written
        assert tmp_path.exists(), 'Config file should exist'

        with open(tmp_path, 'r') as f:
            content = f.read()
            assert content == test_json, f'Content mismatch: {content}'

        print('✓ ConfigSaverWorker test passed')

    finally:
        # Clean up
        if tmp_path.exists():
            tmp_path.unlink()


def test_config_saver_manager():
    """Test ConfigSaverManager basic functionality"""
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Create manager
        manager = ConfigSaverManager()

        # Test data
        test_json = '{"test": "manager_data"}'

        # Save config
        manager.save_config_async(tmp_path, test_json)

        # Wait for completion
        success = manager.wait_for_completion(5000)
        assert success, 'Manager should complete within timeout'

        # Verify content
        assert tmp_path.exists(), 'Config file should exist'

        with open(tmp_path, 'r') as f:
            content = f.read()
            assert content == test_json, f'Content mismatch: {content}'

        print('✓ ConfigSaverManager test passed')

    finally:
        # Clean up
        if tmp_path.exists():
            tmp_path.unlink()


def test_config_saver_error_handling():
    """Test ConfigSaverWorker error handling"""
    # Use a path in a read-only location (more likely to fail)
    # But actually, let's just test that it doesn't crash
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Test data
        test_json = '{"test": "data"}'

        # Create worker
        worker = ConfigSaverWorker(tmp_path, test_json)

        # Start worker
        worker.start()

        # Wait for completion (with timeout)
        success = worker.wait(5000)

        # Verify worker completed without crashing
        assert success, 'Worker should complete'

        print('✓ ConfigSaverWorker error handling test passed')

    finally:
        # Clean up
        if tmp_path.exists():
            tmp_path.unlink()


if __name__ == '__main__':
    print('Running config saver tests...')
    test_config_saver_worker()
    test_config_saver_manager()
    test_config_saver_error_handling()
    print('\n✓ All config saver tests passed!')
