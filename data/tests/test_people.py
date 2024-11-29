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
WITHSUBDOMAIN = "jane.smith@mail.example.com"
WITHSPECIALCHARS = "alice+johnson@example.co.uk"

TEMP_EMAIL = 'bvvdIsTrash@trasch.bvvd'

# ppl.create("Jane Smith", "NYU", "jjane.smith@mail.example.com", "")
# ppl.create("Alice Johnson", "NYU", "alice+johnson@example.co.uk", "")



@pytest.fixture(scope='function')
def temp_person():
    _id = ppl.create('Cybercricetus', 'BVVD', TEMP_EMAIL, TEST_ROLE_CODE)
    yield _id
    try:
        ppl.delete(_id)
    except:
        print('Person already deleted.')


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


def test_with_subdomain():
    assert ppl.is_valid_email(WITHSUBDOMAIN)


def test_with_special_chars():
    assert ppl.is_valid_email(WITHSPECIALCHARS)


def test_read(temp_person):
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


def test_exists(temp_person):
    assert ppl.exists(temp_person)


def test_doesnt_exist():
    assert not ppl.exists('Not an existing email.')


def test_delete(temp_person):
    ppl.delete(temp_person)
    assert not ppl.exists(temp_person)


ADD_EMAIL = 'yuzuka@nyu.edu'


def test_create_person():
    ppl.create('Yuzuka Rao', 'NYU', ADD_EMAIL, TEST_ROLE_CODE)
    assert ppl.exists(ADD_EMAIL)
    '''
        Make sure the tested email is cleaned.
    '''
    ppl.delete(ADD_EMAIL)


def test_create_duplicate(temp_person):
    with pytest.raises(ValueError):
        ppl.create('Repeated Name', 'Affiliation', temp_person, TEST_ROLE_CODE)


# def test_create_bad_email():
#     with pytest.raises(ValueError):
#         ppl.create_people('Do not care about name',
#                           'Affiliation', 'bademail', TEST_CODE)
NONEXIST_EMAIL = 'eric@nyu.edu'
TEST_AFF = "steam"


# @pytest.mark.skip("This test is not working")
def test_set_affilation(temp_person):
    people = ppl.read_one(temp_person)
    old_aff = people[ppl.AFFILIATION]
    ppl.set_affiliation(TEMP_EMAIL, TEST_AFF)
    people = ppl.read()  # read new info
    assert old_aff != people[TEMP_EMAIL][ppl.AFFILIATION]
    assert people[TEMP_EMAIL][ppl.AFFILIATION] == TEST_AFF


def test_set_affilation_not_exist():
    people = ppl.read()
    res = ppl.set_affiliation(NONEXIST_EMAIL, TEST_AFF)
    assert not res


VALID_ROLES = ['ED', 'AU']


def test_update(temp_person):
    ppl.update('Buffalo Bill', 'UBuffalo', temp_person, VALID_ROLES)
    updated_rec = ppl.read_one(temp_person)
    assert updated_rec[ppl.NAME] == 'Buffalo Bill'


def test_update_not_there(temp_person):
    with pytest.raises(ValueError):
        ppl.update('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
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


@patch('data.roles.is_valid', return_value=False)
def test_is_valid_person_with_invalid_role(mock_is_valid):
    with pytest.raises(ValueError, match="Invalid role:"):
        ppl.is_valid_person(name="Alice", affiliation="University", email="alice@domain.com", role="INVALID")
    mock_is_valid.assert_called_once_with("INVALID")

