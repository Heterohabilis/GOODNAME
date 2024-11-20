import pytest

from unittest.mock import patch

import data.people as ppl

import data.db_connect as dbc   

from data.roles import TEST_CODE as TEST_ROLE_CODE


ATLESS = 'cybercricetus'
NAMELESS = '@nyu.edu'
DOMAINLESS = 'cybercricetus@'
FULL = "cybercricetus@nyu.edu"
SPECIALCHARS = "elaine#e@nyu.edu"
WITHUNDERSCORE = "elaine_ll@nyu.edu"
WITHDOT = "elaine.ll@nyu.edu"
WITHDASH = "elaine-ll@nyu.edu"
STARTWITHDOT = ".elaine@nyu.edu"
ENDWITHDASH = "elaine-@nyu.edu"
CONSECUTIVEDOTS = "elaine..ll@nyu.edu"
DOMAINLASTMISSING = "elaine@nyu"
DOMAINSPECIALCHARS = "elaine@nyu#archive.edu"
DOMAINCONSECUTIVEDOTS = "elaine@nyu..edu"
DOMAINSTARTWITHDOT = "elaine@.nyu.edu"
DOMAINLESSTHANTWOCHARS = "elaine@nyu.e"
DOMAINMORETHANTWOCHARS = "elaine@nyu.ed"
DOMAINWITHDASH = "elaine@nyu-archive.edu"
DOMAINENDWITHDASH = "elaine@nyu-.edu"

TEMP_EMAIL = 'bvvdIsTrash@trash.bvvd'


@pytest.fixture(scope='function')
def temp_person():
    _id = ppl.create_person('Cybercricetus', 'BVVD', TEMP_EMAIL, TEST_ROLE_CODE)
    yield _id
    ppl.delete(_id)


@pytest.fixture(scope='function')
def temp_person_for_test_del():
    _id = ppl.create_person(ppl.DEL_EMAIL, 'NYU', ppl.DEL_EMAIL, 'ED')
    yield _id


def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


def test_create_mh_rec(temp_person):
    person_rec = ppl.read_one(temp_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec


def test_has_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)


def test_doesnt_have_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert not ppl.has_role(person_rec, 'Not a good role!')



def test_is_mail_valid_atless():
    assert not ppl.is_valid_email(ATLESS)


def test_is_mail_valid_nameless():
    assert not ppl.is_valid_email(NAMELESS)


def test_is_mail_valid_domainless():
    assert not ppl.is_valid_email(DOMAINLESS)


def test_is_mail_valid_full():
    assert ppl.is_valid_email(FULL)


def test_has_special_chars():
    assert not ppl.is_valid_email(SPECIALCHARS)


def test_has_underscore():
    assert ppl.is_valid_email(WITHUNDERSCORE)


def test_has_dot():
    assert ppl.is_valid_email(WITHDOT)


def test_has_dash():
    assert ppl.is_valid_email(WITHDASH)


def test_start_with_dot():
    assert not ppl.is_valid_email(STARTWITHDOT)


def test_end_with_dash():
    assert not ppl.is_valid_email(ENDWITHDASH)


def test_consecutive_dots():
    assert not ppl.is_valid_email(CONSECUTIVEDOTS)


def test_domain_last_missing():
    assert not ppl.is_valid_email(DOMAINLASTMISSING)


def test_domain_special_chars():
    assert not ppl.is_valid_email(DOMAINSPECIALCHARS)


def test_domain_consecutive_dots():
    assert not ppl.is_valid_email(DOMAINCONSECUTIVEDOTS)


def test_domain_start_with_dot():
    assert not ppl.is_valid_email(DOMAINSTARTWITHDOT)


def test_domain_less_than_two_chars():
    assert not ppl.is_valid_email(DOMAINLESSTHANTWOCHARS)


def test_domain_more_than_two_chars():
    assert ppl.is_valid_email(DOMAINMORETHANTWOCHARS)


def test_domain_with_dash():
    assert ppl.is_valid_email(DOMAINWITHDASH)


def test_domain_end_with_dash():
    assert not ppl.is_valid_email(DOMAINENDWITHDASH)


def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    assert ppl.read_one('Not an existing email!') is None


def test_delete_person(temp_person_for_test_del):
    people = ppl.read()
    old_len = len(people)
    ppl.delete(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


ADD_EMAIL = 'yuzuka@nyu.edu'


def test_create_person():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create_person('Yuzuka Rao', 'NYU', ADD_EMAIL, TEST_ROLE_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people
    '''
        Make sure the tested email is cleaned.
    '''
    ppl.delete(ADD_EMAIL)


def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create_person('Repeated Name', 'Affiliation', ppl.TEST_EMAIL, TEST_ROLE_CODE)


# def test_create_bad_email():
#     with pytest.raises(ValueError):
#         ppl.create_people('Do not care about name',
#                           'Affiliation', 'bademail', TEST_CODE)
NONEXIST_EMAIL = 'eric@nyu.edu'
TEST_AFF = "steam"


def test_set_affilation():
    people = ppl.read()
    old_aff = people[ppl.TEST_EMAIL][ppl.AFFILIATION]
    ppl.set_affiliation(ppl.TEST_EMAIL, TEST_AFF)
    people = ppl.read()  # read new info
    assert old_aff != people[ppl.TEST_EMAIL][ppl.AFFILIATION]
    assert people[ppl.TEST_EMAIL][ppl.AFFILIATION] == TEST_AFF
    ppl.set_affiliation(ppl.TEST_EMAIL, "NYU") # recover to original state


def test_set_affilation_not_exist():
    people = ppl.read()
    res = ppl.set_affiliation(NONEXIST_EMAIL, TEST_AFF)
    assert not res


VALID_ROLES = ['ED', 'AU']


@pytest.mark.skip('Skipping cause not done.')
def test_update(temp_person):
    ppl.update('Buffalo Bill', 'UBuffalo', temp_person, VALID_ROLES)


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                   'Or affiliation', 'bademail', TEST_ROLE_CODE)


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)


TEST_ROLES_BVVD = ['trash gamer', 'trash game', 'trash company']


def test_fancy_is_valid_person():
    with pytest.raises(ValueError):
        '''
        Test invalid email... this should raise ValueError exception
        '''
        ppl.is_valid_person("bvvd", "Gaijin Inc", "bvvd@bvvdIsSuck")

    with pytest.raises(ValueError):
        '''
        Test invalid, single role... this should also raise ValueError
        '''
        ppl.is_valid_person("bvvd", "Gaijin Inc", "bvvd@isTrash.com", "DV")

    with pytest.raises(ValueError):
        '''
        Test invalid, role list... this should also raise ValueError
        '''
        ppl.is_valid_person("bvvd", "Gaijin Inc", "bvvd@isTrash.com", None, TEST_ROLES_BVVD)


@patch('data.people.read', return_value={'test@domain.com': {'name': 'Test User'}})
def test_get_person_success(mock_read):
    person = ppl.get_person('test@domain.com')
    assert person == {'name': 'Test User'}
    mock_read.assert_called_once()  


@patch('data.people.read', return_value={})
def test_get_person_not_found(mock_read):
    person = ppl.get_person('nonexistent@domain.com')
    assert person is None
    mock_read.assert_called_once()


@patch('data.roles.is_valid', return_value=False)
def test_is_valid_person_with_invalid_role(mock_is_valid):
    with pytest.raises(ValueError, match="Invalid role:"):
        ppl.is_valid_person(name="Alice", affiliation="University", email="alice@domain.com", role="INVALID")
    mock_is_valid.assert_called_once_with("INVALID")

