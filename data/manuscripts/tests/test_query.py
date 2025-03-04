import random

import pytest

import data.manuscripts.query as mqry


def gen_random_not_valid_str() -> str:
    """
    That huge number is only important in being huge:
        any big number would do.
    """
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())
        

def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_not_valid_action():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


_id = 'id'


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_valid_return():
    for state in mqry.get_states():
        print(state)
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{action=}')
            new_state = mqry.handle_action(state, action,
                                           manu=mqry.SAMPLE_MANU,
                                           referee='Some ref')
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)


@pytest.fixture(scope='function')
def temp_manu():
    id_ = mqry.create("a", "b", "c", "d", "e", "g")
    yield id_
    mqry.delete(id_)


TEST_ID = '675e6b4f7a057d0f581d3dee'


def test_exist(temp_manu):
    assert mqry.exists(temp_manu)


def test_not_exist():
    assert not mqry.exists(TEST_ID)


def test_create():
    id_ = mqry.create("a", "b", "c", "d", "e", "g")
    assert mqry.exists(id_)
    mqry.delete(id_)


def test_update(temp_manu):
    updated_title, updated_author, updated_author_email, updated_text, updated_abstract, updated_editor= "a", "a", "a", "a", "a", "a"
    mqry.update(temp_manu, updated_title, updated_author, updated_author_email, updated_text, updated_abstract, updated_editor)
    updated_manu = mqry.read_one(temp_manu)
    assert updated_manu[mqry.flds.TITLE] == updated_title
    assert updated_manu[mqry.flds.AUTHOR] == updated_author
    assert updated_manu[mqry.flds.AUTHOR_EMAIL] == updated_author_email
    assert updated_manu[mqry.flds.TEXT] == updated_text
    assert updated_manu[mqry.flds.ABSTRACT] == updated_abstract
    assert updated_manu[mqry.flds.EDITOR] == updated_editor


def test_update_failed():
    with pytest.raises(ValueError):
        mqry.update(TEST_ID, 'a', 'b', 'c', 'd', 'e', 'g')


def test_delete(temp_manu):
    assert mqry.exists(temp_manu)
    ret = mqry.delete(temp_manu)
    assert ret


def test_invalid_delete():
    assert not mqry.exists(TEST_ID)
    ret = mqry.delete(TEST_ID)
    assert not ret


def test_read(temp_manu):
    assert len(mqry.read())>0


def test_read_one(temp_manu):
    assert mqry.read_one(temp_manu)


def test_read_one_invalid():
    assert not mqry.read_one(TEST_ID)


def test_assign_ref(temp_manu):
    ref = "Reviewer1"
    manu = mqry.read_one(temp_manu)
    new_state = mqry.assign_ref(manu, ref)
    assert new_state == mqry.IN_REF_REV
    assert ref in manu[mqry.flds.REFEREES]


def test_delete_ref(temp_manu):
    ref = "Reviewer1"
    manu = mqry.read_one(temp_manu)
    mqry.assign_ref(manu, ref)
    new_state = mqry.delete_ref(manu, ref)
    assert new_state == mqry.SUBMITTED
    assert ref not in manu[mqry.flds.REFEREES]


def test_delete_ref_with_multiple_refs(temp_manu):
    refs = ["Reviewer1", "Reviewer2"]
    manu = mqry.read_one(temp_manu)
    for ref in refs:
        mqry.assign_ref(manu, ref)
    new_state = mqry.delete_ref(manu, "Reviewer1")
    assert new_state == mqry.IN_REF_REV
    assert "Reviewer1" not in manu[mqry.flds.REFEREES]
    assert "Reviewer2" in manu[mqry.flds.REFEREES]


# def test_update_state(temp_manu):
#     new_state = mqry.update_state(temp_manu, mqry.SUBMITTED, mqry.ASSIGN_REF, ref='Alice')
#     assert new_state == mqry.IN_REF_REV
