import pytest

import data.people as ppl

from data.roles import TEST_CODE

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


def test_del_person():
    people = ppl.read()
    old_len = len(people)
    ppl.delete_person(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


ADD_EMAIL = 'yuzuka@nyu.edu'


def test_create_person():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create_person('Yuzuka Rao', 'NYU', ADD_EMAIL, TEST_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create_person('Repeated Name', 'Affiliation', ppl.TEST_EMAIL, TEST_CODE)


# def test_create_bad_email():
#     with pytest.raises(ValueError):
#         ppl.create_people('Do not care about name',
#                           'Affiliation', 'bademail', TEST_CODE)


def test_get_person():
    people = ppl.read()
    person = ppl.get_person(ppl.TEST_EMAIL)
    assert isinstance(person, dict)


NONEXIST_EMAIL = 'eric@nyu.edu'


def test_get_person_not_exist():
    people = ppl.read()
    person = ppl.get_person(NONEXIST_EMAIL)
    assert person is None


TEST_AFF = "steam"


def test_set_affilation():
    people = ppl.read()
    old_aff = people[ppl.TEST_EMAIL][ppl.AFFILIATION]
    ppl.set_affiliation(ppl.TEST_EMAIL, TEST_AFF)
    assert old_aff != people[ppl.TEST_EMAIL][ppl.AFFILIATION]
    assert people[ppl.TEST_EMAIL][ppl.AFFILIATION] == TEST_AFF


def test_set_affilation_not_exist():
    people = ppl.read()
    res = ppl.set_affiliation(NONEXIST_EMAIL, TEST_AFF)
    assert not res


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                   'Or affiliation', 'bademail', TEST_CODE)
