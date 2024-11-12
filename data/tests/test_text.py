from unittest.mock import patch

import pytest

import data.text as txt

ADD_KEY = 'AddPage'


@pytest.fixture(scope='function')
def temp_text():
    txt.create(ADD_KEY, 'Add Page', 'This is a page to add.', 'mock_email')
    yield ADD_KEY
    txt.delete(ADD_KEY)


def test_read():
    text_data = txt.read()
    assert isinstance(text_data, dict)
    assert len(text_data) > 0
    for _id, text in text_data.items():
        assert isinstance(_id, str)
        assert txt.TITLE in text
        assert txt.TEXT in text


def test_read_one():
    assert len(txt.read_one(txt.TEST_KEY)) > 0


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}


def test_delete():
    text_data = txt.read()
    old_len = len(text_data)
    txt.delete(txt.DEL_KEY)
    text_data = txt.read()
    assert len(text_data) < old_len
    assert txt.DEL_KEY not in text_data


def test_create():
    text_data = txt.read()
    assert ADD_KEY not in text_data
    txt.create(ADD_KEY, 'Add Page', 'This is a page to add.', 'mock_email')


@pytest.mark.skip('Not completed')
def test_update(temp_text):
    txt.update(ADD_KEY, 'Add Page', 'This is a page to add.', 'mock_email')
