import data.text as tx

def test_read():
    text_data = tx.read()
    assert isinstance(text_data, dict)
    assert len(text_data) > 0
    for _id, text in text_data.items():
        assert isinstance(_id, str)
        assert tx.TITLE in text
        assert tx.TEXT in text
