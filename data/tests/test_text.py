from unittest.mock import patch

import pytest

import data.text as txt

ADD_TITLE = 'Add Page'


@pytest.fixture(scope='function')
def temp_text():
    txt.create(ADD_TITLE, 'This is a page to add.', 'mock_email')
    yield ADD_TITLE
    txt.delete(ADD_TITLE)


def test_exist(temp_text):
    assert txt.exists(temp_text)


def test_not_exist():
    assert not txt.exists('Not a page key!')


def test_read(temp_text):
    text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0
    for key, page in text.items():
        assert isinstance(key, str)
        assert isinstance(page, dict)


def test_read_one(temp_text):
    assert txt.read_one(temp_text) is not None


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') is None


def test_delete(temp_text):
    txt.delete(temp_text)
    assert txt.read_one(temp_text) is None


def test_create():
    assert not txt.exists(ADD_TITLE)
    txt.create(ADD_TITLE, 'This is a page to add.', 'mock_email')
    assert txt.exists(ADD_TITLE)
    txt.delete(ADD_TITLE)


def test_create_duplicate(temp_text):
    with pytest.raises(ValueError):
        txt.create(ADD_TITLE, 'This is a page to add.', 'mock_email')


def test_update(temp_text):
    txt.update(ADD_TITLE, 'This is an updated page.', 'mock_email')
    updated_text = txt.read_one(temp_text)
    assert updated_text[txt.TEXT] == 'This is an updated page.'


def test_update_not_found():
    with pytest.raises(ValueError):
        txt.update('Null Title', 'This is an updated page.', 'mock_email')
