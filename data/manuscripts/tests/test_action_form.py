import pytest

import data.manuscripts.action_form as af


def test_form_return() -> None:
    assert af.get_form() is not None
