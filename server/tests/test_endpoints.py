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


@patch('data.people.read', autospec=True,
       return_value={'id': {NAME: 'Elaine Li'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


@patch('data.people.read_one', autospec=True,
       return_value={NAME: 'Yuzuka Rao'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK
    
    
def test_get_text():
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    for key, page in resp_json.items():
        assert isinstance(key, str)
        assert len(key) > 0
        assert TITLE in page


@patch('data.people.delete_person', autospec=True, return_value='mock_id')
def test_delete_person_success(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/mock_id')
    resp_json = resp.get_json()
    assert resp.status_code == OK
    assert resp_json == {'Deleted': 'mock_id'}


@patch('data.people.delete_person', autospec=True, return_value=None)
def test_delete_person_not_there(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


@patch('data.people.create_person', autospec=True, return_value='mock_email')
@patch('data.people.is_valid_email', autospec=True, return_value=True)
def test_create_person_success(mock_create, mock_is_valid):
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create',
                           json={'name': 'name', 'affiliation': 'affiliation', 'email': 'mock_email'})
    assert resp.status_code == OK
    assert resp.json == {ep.MESSAGE: 'Person added!', ep.RETURN: 'mock_email'}


@patch('data.people.create_person', autospec=True, return_value='mock_email')
@patch('data.people.is_valid_email', autospec=True, return_value=False)
def test_create_person_invalid(mock_create, mock_is_valid):
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create',
                           json={'name': 'name', 'affiliation': 'affiliation', 'email': 'mock_email'})
    assert resp.status_code == OK
    assert resp.json == {
        ep.MESSAGE: 'Wrong Email Format',
        ep.RETURN: None
    }


@patch('data.people.create_person', autospec=True, side_effect=ValueError)
@patch('data.people.is_valid_email', autospec=True)
def test_create_person_error(mock_create, mock_is_valid):
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create',
                           json={'name': 'name', 'affiliation': 'affiliation', 'email': 'mock_email'})
    assert resp.status_code == NOT_ACCEPTABLE

