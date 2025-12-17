from dnf_db.model import Postal
from dnf_db.repo.postal_repo import get_postal_repo


def test_query_all():
    repo = get_postal_repo()
    item_list = repo.query_all()
    for item in item_list:
        print(item.__dict__)


def test_delete_by_id():
    """Test the delete_by_id functionality"""
    repo = get_postal_repo()

    # First, create a test postal item
    test_postal = Postal.default()
    test_postal.send_character_name = 'test_delete'
    test_postal.receive_character_no = 999999  # Use a test character number
    test_postal.item_id = 12345

    # Add the test postal item
    added_postal = repo.add(test_postal)
    postal_id = added_postal.postal_id
    print(f'Created test postal with ID: {postal_id}')

    # Verify it exists
    found_postal = repo.query_by_id(postal_id)
    assert found_postal is not None, 'Test postal should exist after creation'
    print(f'Verified postal exists: {found_postal.send_character_name}')

    # Delete it
    deletion_success = repo.delete_by_id(postal_id)
    assert deletion_success, 'Deletion should return True for existing postal'
    print(f'Deletion successful: {deletion_success}')

    # Verify it's gone
    deleted_postal = repo.query_by_id(postal_id)
    assert deleted_postal is None, 'Postal should not exist after deletion'
    print('Verified postal was deleted successfully')

    # Test deleting non-existent postal
    non_existent_deletion = repo.delete_by_id(999999999)
    assert not non_existent_deletion, 'Deleting non-existent postal should return False'
    print(f'Non-existent deletion returned: {non_existent_deletion}')

    print('All delete_by_id tests passed!')
