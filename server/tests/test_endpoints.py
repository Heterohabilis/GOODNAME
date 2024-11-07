from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

from data.people import NAME, DEL_EMAIL

from data.text import TITLE

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


# Journal Name Retrieval testcase
def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    print(f'{ep.TITLE_EP=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


# My testcase
def test_cricetus():
    resp = TEST_CLIENT.get(ep.CRICETUS_EP)
    resp_json = resp.get_json()
    assert ep.CRICETUS_RESP in resp_json


def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


def test_get_text():
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    for key, page in resp_json.items():
        assert isinstance(key, str)
        assert len(key) > 0
        assert TITLE in page


def test_delete_person_success():
    with patch('data.people.delete_person') as mock_delete_person:
        mock_delete_person.return_value = DEL_EMAIL
        resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{DEL_EMAIL}')
        assert resp.status_code == OK
        assert resp.json == {'Deleted': DEL_EMAIL}
        mock_delete_person.assert_called_once_with(DEL_EMAIL)


# NOT_EXIST_EMAIL = 'not_exist'
# def test_delete_person_not_there():
#     resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{NOT_EXIST_EMAIL}')
#     assert resp.status_code == NOT_FOUND
#     assert resp.json == {'No such person': NOT_EXIST_EMAIL}


def test_create_person_success():
    with patch('data.people.create_person') as mock_create_person:
        email = 'new_email@gmail.com'
        mock_create_person.return_value = email
        resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json={'name': 'name', 'affiliation': 'affiliation', 'email': email})
        assert resp.status_code == OK
        assert resp.json == {ep.MESSAGE: 'Person added!', ep.RETURN: 'new_email@gmail.com'}
        mock_create_person.assert_called_once_with('name', 'affiliation', email, None)


def test_create_person_invalid():
    with patch('data.people.is_valid_email') as mock_is_valid_email:
        mock_is_valid_email.return_value = False
        email = 'invalid_email'
        resp = TEST_CLIENT.put(
            f'{ep.PEOPLE_EP}/create',
            json={
                'name': NAME,
                'affiliation': 'affiliation',
                'email': email
            }
        )

        assert resp.status_code == OK
        assert resp.json == {
            ep.MESSAGE: 'Wrong Email Format',
            ep.RETURN: None
        }
        mock_is_valid_email.assert_called_once_with(email)


def test_create_person_error():
    with patch('data.people.is_valid_email') as mock_is_valid_email, \
            patch('data.people.create_person') as mock_create_person:
        mock_is_valid_email.return_value = True
        mock_create_person.side_effect = Exception('Database error')
        resp = TEST_CLIENT.put(
            f'{ep.PEOPLE_EP}/create',
            json={
                'name': NAME,
                'affiliation': 'affiliation',
                'email': 'email'
            }
        )

        # Assert 406 Not Acceptable with error message
        assert resp.status_code == NOT_ACCEPTABLE
        expected_message = f"Could not add person: err=Exception('Database error')"
        assert resp.json['message'] == expected_message

