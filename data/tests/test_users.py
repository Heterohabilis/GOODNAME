import pytest
import data.users as us

TEST_USERNAME = "test_user"
TEST_PASSWORD = "test_password"
TEST_LEVEL = 1
TEST_NAME = 'test_name'


@pytest.fixture(scope='function')
def temp_user():
    us.add_user(TEST_USERNAME, TEST_PASSWORD, TEST_NAME, TEST_LEVEL)
    yield TEST_USERNAME
    us.delete_user(TEST_USERNAME)


def test_exists(temp_user):
    assert us.exists(temp_user)


def test_not_exists():
    assert not us.exists("non_existent_user")


def test_add_user():
    us.delete_user(TEST_USERNAME)
    result = us.add_user(TEST_USERNAME, TEST_PASSWORD, TEST_NAME, TEST_LEVEL)
    assert "message" in result
    assert us.exists(TEST_USERNAME)
    us.delete_user(TEST_USERNAME)


def test_add_user_duplicate(temp_user):
    result = us.add_user(temp_user,  TEST_PASSWORD, TEST_NAME, TEST_LEVEL)
    assert "error" in result


def test_delete_user(temp_user):
    result = us.delete_user(temp_user)
    assert "message" in result
    assert not us.exists(temp_user)


def test_delete_user_not_found():
    result = us.delete_user("ghost_user")
    assert "error" in result


def test_update_user(temp_user):
    new_level = 5
    result = us.update_user(TEST_USERNAME, TEST_PASSWORD, new_level)
    assert "message" in result
    users = us.get_users()
    assert users[TEST_USERNAME][us.LEVEL] == new_level


def test_update_user_not_found():
    result = us.update_user("ghost_user", "pass", 3)
    assert "error" in result


def test_get_users(temp_user):
    users = us.get_users()
    assert isinstance(users, dict)
    assert temp_user in users
    assert isinstance(users[temp_user], dict)
    assert us.LEVEL in users[temp_user]