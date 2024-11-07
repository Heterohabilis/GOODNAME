import data.text as txt

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