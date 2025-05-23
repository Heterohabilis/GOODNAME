import pytest
import security.security as sec
import data.users as users
import data.people as people
from unittest.mock import patch


# Dummy user records
users.get_users = lambda: {
    "tt33@we.pn": {
        "username": "tt33@we.pn",
        "level": 0
    },
    "xm2204@nyu.edu": {
        "username": "xm2204@nyu.edu",
        "level": 1
    }
}


people.read_one = lambda email: None if email == "non-existent user" else {
    "name": "Test",
    "affiliation": "Dept",
    "roles": ["ED"] if email == "xm2204@nyu.edu" else ["AU"]
}


def test_check_login_good():
    assert sec.check_login(sec.GOOD_USER_ID,
                           login_key='any key will do for now')


def test_check_login_bad():
    assert not sec.check_login(sec.GOOD_USER_ID)


def test_read():
    recs = sec.read()
    assert isinstance(recs, dict)
    for feature in recs:
        assert isinstance(feature, str)
        assert len(feature) > 0


def test_read_feature():
    feature = sec.read_feature(sec.PEOPLE)
    assert isinstance(feature, dict)


def test_is_permitted_no_such_feature():
    assert sec.is_permitted('Non-existent feature', sec.CREATE, 'any user')


def test_is_permitted_action_missing():
    assert sec.is_permitted(sec.PEOPLE, sec.PEOPLE_MISSING_ACTION, 'any user')


@patch('data.people.read_one', return_value=None)
def test_is_permitted_bad_user(mock_read):
    assert not sec.is_permitted(sec.PEOPLE, sec.CREATE, 'non-existent user')


def test_is_permitted_bad_check():
    with pytest.raises(ValueError):
        sec.is_permitted(sec.BAD_FEATURE, sec.CREATE, sec.GOOD_USER_ID)


def test_is_permitted_level_admin_pass():
    assert sec.is_permitted(sec.PEOPLE, sec.UPDATE, "xm2204@nyu.edu")

def test_is_permitted_level_admin_fail():
    assert not sec.is_permitted(sec.PEOPLE, sec.UPDATE, 'tt33@we.pn')