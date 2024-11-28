COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
TEST_STATE = SUBMITTED

VALID_STATES = [
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
]


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS