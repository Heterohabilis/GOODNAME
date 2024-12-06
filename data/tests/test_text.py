from unittest.mock import patch

import pytest

import data.text as txt

ADD_KEY = 'AddPage'


@pytest.fixture(scope='function')
def temp_text():
    txt.create(ADD_KEY, 'This is a page to add.', 'mock_email')
    yield ADD_KEY
    txt.delete(ADD_KEY)


def test_read(temp_text):
    text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0
    for key, page in text.items():
        assert isinstance(key, str)
        assert isinstance(page, dict)


def test_read_one(temp_text):
    assert txt.read_one(temp_text) != {}


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}


def test_delete(temp_text):
    assert txt.delete(temp_text) == temp_text
    assert txt.read_one(temp_text) == {}


def test_create():
    text_data = txt.read()
    assert ADD_KEY not in text_data
    txt.create('Add Page', 'This is a page to add.', 'mock_email')
    text_data = txt.read()
    assert ADD_KEY in text_data
    txt.delete(ADD_KEY)


def test_create_duplicate(temp_text):
    with pytest.raises(ValueError):
        txt.create(ADD_KEY, 'This is a page to add.', 'mock_email')


def test_update(temp_text):
    txt.update(ADD_KEY, 'Add Page', 'This is an updated page.', 'mock_email')
    updated_text = txt.read_one(ADD_KEY)
    assert updated_text[txt.TEXT] == 'This is an updated page.'
