from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE, UNAUTHORIZED,
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
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id/someone')
    assert resp.status_code == OK
    assert resp.json == {ep.NAME: 'Yuzuka Rao'}


@patch('data.people.read_one', autospec=True, return_value=None)
def test_read_one_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


PERSON_PATH = f"{ep.PEOPLE_EP}/mock_id/test_user"
@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.people.delete', autospec=True, return_value='mock_id')
def test_delete_person_success(_, mock_delete):
    resp = TEST_CLIENT.delete(PERSON_PATH)
    assert resp.status_code == OK


@patch('data.people.delete', autospec=True, return_value=None)
def test_delete_person_not_there(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.people.update', autospec=True, return_value='mock_email')
@patch('data.people.is_valid_email', autospec=True, return_value=True)
def test_update_person(_, mock_update, mock_is_valid):
    resp = TEST_CLIENT.put(
        PERSON_PATH,
        json={'name': 'name', 'affiliation': 'affiliation', 'roles': 'roles'}
    )
    assert resp.status_code == OK
    assert resp.json == {ep.MESSAGE: 'Person updated!', ep.RETURN: 'mock_email'}


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.people.update', autospec=True, side_effect=ValueError)
@patch('data.people.is_valid_email', autospec=True)
def test_update_person_error(_, mock_update, mock_is_valid):
    resp = TEST_CLIENT.put(
        PERSON_PATH,
        json={'name': 'name', 'affiliation': 'affiliation', 'roles': 'roles'}
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.people.create', autospec=True, return_value='mock_email')
@patch('data.people.is_valid_email', autospec=True, return_value=True)
@patch('security.security.is_permitted', autospec=True, return_value=True)
def test_create_person_success(mock_create, mock_is_valid, mock_is_permitted):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/create?user_id=test_user',
        json={'name': 'name', 'affiliation': 'affiliation', 'email': 'mock_email', 'roles': 'Editor'}
    )
    assert resp.status_code == OK
    assert resp.json == {ep.MESSAGE: 'Person added!', ep.RETURN: 'mock_email'}



@patch('data.people.create', autospec=True, side_effect=ValueError)
@patch('data.people.is_valid_email', autospec=True)
@patch('security.security.is_permitted', autospec=True, return_value=True)
def test_create_person_error(mock_create, mock_is_valid, mock_is_permitted):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/create?user_id=test_user',
        json={'name': 'name', 'affiliation': 'affiliation', 'email': 'mock_email', 'roles': 'Editor'}
    )
    assert resp.status_code == NOT_ACCEPTABLE



@patch('data.text.read', autospec=True, return_value={'key': {TITLE: 'Title'}})
def test_get_text(mock_read):
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for key, text in resp_json.items():
        assert isinstance(key, str)
        assert len(key) > 0
        assert TITLE in text


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.read_one', autospec=True, return_value={TITLE: 'Title'})
def test_get_text_one(mock_read_one, mock_is_permitted):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/key/user_id')
    assert resp.status_code == OK


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.read_one', autospec=True, return_value=None)
def test_get_text_one_not_found(mock_read_one, mock_is_permitted):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/key/user_id')
    assert resp.status_code == NOT_FOUND


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.delete', autospec=True, return_value='key')
def test_delete_text(mock_delete, mock_is_permitted):
    resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/key/user_id')
    assert resp.status_code == OK


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.delete', autospec=True, return_value=None)
def test_delete_text_not_found(mock_delete, mock_is_permitted):
    resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/key/user_id')
    assert resp.status_code == NOT_FOUND


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.update', autospec=True, return_value='key')
def test_update_text(mock_update, mock_is_permitted):
    resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/key/user_id',
                           json={'title': 'Title', 'text': 'Text', 'email': 'mock_email'})
    assert resp.status_code == OK
    assert resp.json == {ep.MESSAGE: 'Text updated!', ep.RETURN: 'key'}


@patch('security.security.is_permitted', autospec=True, return_value=True)
@patch('data.text.update', autospec=True, side_effect=ValueError)
def test_update_text_error(mock_update, mock_is_permitted):
    resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/key/user_id',
                           json={'title': 'Title', 'Text': 'text', 'email': 'mock_email'})
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.text.create', autospec=True, return_value='TitlePage')
def test_create_text_success(mock_create):
    resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/create',
                           json={'title': 'Title Page', 'text': 'Text', 'email': 'mock_email'})
    assert resp.status_code == OK


@patch('data.text.create', autospec=True, side_effect=ValueError)
def test_create_text_error(mock_create):
    resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/create',
                           json={'title': 'Title', 'text': 'Text', 'email': 'mock_email'})
    assert resp.status_code == NOT_ACCEPTABLE


# @patch('data.manuscripts.query.update_state', autospec=True, return_value='mock_state')
# def test_update_state(mock_update_state):
#     _id = 'mock_id'
#     action = 'action'
#     resp = TEST_CLIENT.put(f'{ep.MANU_EP}/{_id}/update_state',
#                            json={'action': action})
#     assert resp.status_code == OK
#     assert resp.json['return'] == 'mock_state'


@patch('data.manuscripts.query.read_one', autospec=True, return_value={'id': 'mock_id', 'title': 'Mock Title'})
def test_get_manuscript_success(mock_read_one):
    resp = TEST_CLIENT.get(f'{ep.MANU_EP}/mock_id')
    assert resp.status_code == OK
    assert resp.json == {'id': 'mock_id', 'title': 'Mock Title'}


@patch('data.manuscripts.query.read_one', autospec=True, return_value=None)
def test_get_manuscript_not_found(mock_read_one):
    resp = TEST_CLIENT.get(f'{ep.MANU_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


@patch('data.manuscripts.query.delete', autospec=True, return_value='mock_id')
def test_delete_manuscript_success(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MANU_EP}/mock_id')
    assert resp.status_code == OK
    assert resp.json == {'Deleted': 'mock_id'}


@patch('data.manuscripts.query.delete', autospec=True, return_value=None)
def test_delete_manuscript_not_found(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MANU_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


@patch('data.manuscripts.query.update', autospec=True, return_value='mock_return')
def test_put_manuscript_success(mock_update):
    payload = {
        'title': 'Updated Title',
        'author': 'Updated Author',
        'author_email': 'email@example.com',
        'text': 'Updated Text',
        'abstract': 'Updated Abstract',
        'editor': 'Updated Editor'
    }
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/mock_id', json=payload)
    assert resp.status_code == OK
    assert resp.json == {'Message': 'Manuscript updated!', 'return': 'mock_return'}


@patch('data.manuscripts.query.update', autospec=True, side_effect=Exception('Update error'))
def test_put_manuscript_error(mock_update):
    payload = {
        'title': 'Title',
        'author': 'Author',
        'author_email': 'email@example.com',
        'text': 'Text',
        'abstract': 'Abstract',
        'editor': 'Editor'
    }
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/mock_id', json=payload)
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.manuscripts.query.create', autospec=True, return_value='new_manuscript_id')
def test_create_manuscript_success(mock_create):
    payload = {
        'title': 'New Title',
        'author': 'New Author',
        'author_email': 'email@example.com',
        'text': 'New Text',
        'abstract': 'New Abstract',
        'editor': 'New Editor'
    }
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/create', json=payload)
    assert resp.status_code == OK
    assert resp.json == {'Message': 'Manuscript added!', 'return': 'new_manuscript_id'}


@patch('data.manuscripts.query.create', autospec=True, side_effect=Exception('Creation error'))
def test_create_manuscript_error(mock_create):
    payload = {
        'title': 'Title',
        'author': 'Author',
        'author_email': 'email@example.com',
        'text': 'Text',
        'abstract': 'Abstract',
        'editor': 'Editor'
    }
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/create', json=payload)
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.manuscripts.query.handle_action', autospec=True, return_value='mock_state')
def test_receive_action(mock_handle_action):
    payload = {'_id': 'id', 'curr_state': 'curr_state', 'action': 'action'}
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json=payload)
    assert resp.status_code == OK
    assert resp.json['return'] == 'mock_state'


@patch('data.manuscripts.query.handle_action', autospec=True, side_effect=Exception('State error'))
def test_receive_action_error(mock_state):
    payload = {'_id': 'id', 'curr_state': 'curr_state', 'action': 'action'}
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json=payload)
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.role_form.get_form', autospec=True, return_value={'editor': ['assign', 'review'], 'author': ['submit']})
def test_roles(mock_get_form):
    resp = TEST_CLIENT.get('/roles')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert 'editor' in resp_json
    assert isinstance(resp_json['editor'], list)


@patch('data.manuscripts.action_form.get_form', autospec=True,
       return_value={'submitted': ['assign_editor'], 'review': ['accept', 'reject']})
def test_actions(mock_get_form):
    resp = TEST_CLIENT.get('/actions')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert 'submitted' in resp_json
    assert isinstance(resp_json['submitted'], list)


def test_get_users():
    resp = TEST_CLIENT.get(ep.USER_EP)
    assert resp.status_code == OK


@patch('data.users.verify_password', autospec=True, return_value=True)
def test_login_success(mock_verify_password):
    resp = TEST_CLIENT.put(ep.LOGIN_EP, json={'username': 'username', 'password': 'password'})
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json['message'] == 'Welcome, username!'


@patch('data.users.verify_password', autospec=True, return_value=False)
def test_login_unauthorized(mock_verify_password):
    resp = TEST_CLIENT.put(ep.LOGIN_EP, json={'username': 'username', 'password': 'wrong_password'})
    assert resp.status_code == UNAUTHORIZED
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json['error'] == "Invalid username or password."


@patch('data.users.verify_password', autospec=True, return_value=True)
def test_login_bad_request(mock_verify_password):
    resp = TEST_CLIENT.put(ep.LOGIN_EP, json={'password': 'password'})
    assert resp.status_code == BAD_REQUEST
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json['error'] == "Username is required."


@patch('data.users.verify_password', autospec=True, side_effect=ValueError)
def test_login_not_acceptable(mock_verify_password):
    resp = TEST_CLIENT.put(ep.LOGIN_EP, json={'username': 'username', 'password': 'password'})
    assert resp.status_code == NOT_ACCEPTABLE


@patch('examples.form.get_form_descr', autospec=True, return_value={
    'username': 'Enter your username',
    'password': 'Enter your password'
})
def test_login_form(mock_get_form_descr):
    resp = TEST_CLIENT.get(f'{ep.LOGIN_EP}/form')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert 'username' in resp_json
    assert 'password' in resp_json


def test_developer_endpoints():
    resp = TEST_CLIENT.get('/developer/endpoints')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert 'active_endpoints' in resp_json
    assert isinstance(resp_json['active_endpoints'], list)
    assert ep.HELLO_EP in resp_json['active_endpoints']


def test_developer_params():
    resp = TEST_CLIENT.get('/developer/params')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert 'endpoint_params' in resp_json
    params_map = resp_json['endpoint_params']
    assert isinstance(params_map, dict)
    key = '/people/<email> [PUT]'
    assert key in params_map
    assert isinstance(params_map[key], list)
    assert 'name' in params_map[key]
    login_key = '/login [PUT]'
    assert login_key in params_map
    assert 'username' in params_map[login_key]
    assert 'password' in params_map[login_key]


# Registration endpoint tests
from http import HTTPStatus

@patch('data.users.add_user', autospec=True,
       return_value={'message': "User 'testuser' registered successfully.",
                     'user': {'username': 'testuser', 'name': 'Test User', 'role': 'author',
                              'affiliation':'affiliation', 'level': 0}})
def test_register_success(mock_add_user):
    resp = TEST_CLIENT.post(ep.REGISTER_EP, json={
        'username': 'testuser',
        'password': 'securepass',
        'name': 'Test User',
        'role': 'author',
        'affiliation': 'affiliation'
    })
    assert resp.status_code == HTTPStatus.CREATED
    resp_json = resp.get_json()
    assert 'message' in resp_json
    assert resp_json['user']['username'] == 'testuser'
    assert resp_json['user']['role'] == 'author'


@patch('data.users.add_user', autospec=True, return_value={'error': 'User already exists.'})
def test_register_user_exists(mock_add_user):
    resp = TEST_CLIENT.post(ep.REGISTER_EP, json={
        'username': 'existinguser',
        'password': 'pass',
        'name': 'Existing User',
        'role': 'editor'
    })
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    resp_json = resp.get_json()
    assert 'error' in resp_json


def test_register_missing_username():
    resp = TEST_CLIENT.post(ep.REGISTER_EP, json={
        'password': 'pass',
        'name': 'No Name',
        'role': 'author'
    })
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    resp_json = resp.get_json()
    assert resp_json['error'] == 'Username is required.'


@patch('data.users.get_users', autospec=True, return_value={'testuser': {'username': 'testuser', 'level': 0}})
def test_get_user_success(mock_get_users):
    resp = TEST_CLIENT.get(f'{ep.USER_EP}/testuser')
    assert resp.status_code == OK
    assert resp.get_json()['username'] == 'testuser'


@patch('data.users.get_users', autospec=True, return_value={})
def test_get_user_not_found(mock_get_users):
    resp = TEST_CLIENT.get(f'{ep.USER_EP}/missinguser')
    assert resp.status_code == NOT_FOUND


@patch('data.users.delete_user', autospec=True, return_value='testuser')
def test_delete_user_success(mock_delete_user):
    resp = TEST_CLIENT.delete(f'{ep.USER_EP}/testuser')
    assert resp.status_code == OK
    assert resp.get_json() == {'Deleted': 'testuser'}


@patch('data.users.delete_user', autospec=True, return_value=None)
def test_delete_user_not_found(mock_delete_user):
    resp = TEST_CLIENT.delete(f'{ep.USER_EP}/unknownuser')
    assert resp.status_code == NOT_FOUND


@patch('data.users.update_user', autospec=True, return_value='testuser')
def test_update_user_success(mock_update_user):
    resp = TEST_CLIENT.put(f'{ep.USER_EP}/testuser', json={
        'password': 'newpass',
        'name': 'New Name',
        'affiliation': 'Affiliation',
        'level': 1
    })
    assert resp.status_code == OK
    assert resp.get_json()[ep.MESSAGE] == 'User updated!'


@patch('data.users.update_user', autospec=True, side_effect=ValueError('bad update'))
def test_update_user_error(mock_update_user):
    resp = TEST_CLIENT.put(f'{ep.USER_EP}/testuser', json={
        'password': 'newpass',
        'name': 'New Name',
        'affiliation': 'Affiliation',
        'level': 1
    })
    assert resp.status_code == NOT_ACCEPTABLE


@patch('security.security.check_level_admin', autospec=True, return_value=True)
def test_check_admin_true(mock_check):
    resp = TEST_CLIENT.get('/check_admin/test_admin@nyu.edu')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert resp_json['user_id'] == 'test_admin@nyu.edu'
    assert resp_json['is_admin'] is True


@patch('security.security.check_level_admin', autospec=True, return_value=False)
def test_check_admin_false(mock_check):
    resp = TEST_CLIENT.get('/check_admin/normal_user@nyu.edu')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert resp_json['user_id'] == 'normal_user@nyu.edu'
    assert resp_json['is_admin'] is False
