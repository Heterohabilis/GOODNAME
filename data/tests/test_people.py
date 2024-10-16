import pytest

import data.people as ppl


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
    ppl.create_people('Yuzuka Rao', 'NYU', ADD_EMAIL)
    people = ppl.read()
    assert ADD_EMAIL in people

def test_get_person():
    people = ppl.read()
    person = ppl.get_person(ppl.TEST_EMAIL)
    assert isinstance(person, dict)

NONEXIST_EMAIL = 'eric@nyu.edu'

def test_get_person_not_exist():
    people = ppl.read()
    person = ppl.get_person(NONEXIST_EMAIL)
    assert person is None

