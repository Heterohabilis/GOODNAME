import data.role_form as rf


def test_form_return() -> None:
    assert rf.get_form() is not None