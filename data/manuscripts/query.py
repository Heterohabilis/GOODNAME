import data.manuscripts.field as flds

AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
EDITOR_REV = 'EDR'
AUTHOR_REVISION = 'ARV'
FORMATTING = 'FMT'
PUBLISHED = 'PUB'
TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    EDITOR_REV,
    AUTHOR_REVISION,
    FORMATTING,
    PUBLISHED,
]


SAMPLE_MANU = {
    flds.TITLE: 'Short module import names in Python',
    flds.AUTHOR: 'Eugene Callahan',
    flds.REFEREES: [],
}


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'
REMOVE_REF = 'RRF'
SUBMIT_REVIEW = 'SBR'
WITHDRAW = 'WDR'
ACCEPT_WITH_REVISIONS = 'AWR'

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
    REMOVE_REF,
    SUBMIT_REVIEW,
    WITHDRAW,
    ACCEPT_WITH_REVISIONS,
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def sub_assign_ref(manu: dict) -> str:
    return IN_REF_REV


FUNC = 'f'

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            # These next lines are alternatives that work the same.
            # FUNC: sub_assign_ref,
            FUNC: lambda m: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            FUNC: lambda m: COPY_EDIT,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
        ACCEPT_WITH_REVISIONS: {
            FUNC: lambda m: AUTHOR_REVISION,
        },
        REMOVE_REF: {
            FUNC: lambda m: SUBMITTED,
        },
        SUBMIT_REVIEW: {
            FUNC: lambda m: IN_REF_REV,
        },
        ASSIGN_REF: {
            FUNC: lambda m: IN_REF_REV,
        },
    },
    AUTHOR_REVISION: {
        DONE: {
            FUNC: lambda m: EDITOR_REV,
        },
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda m: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {
        DONE: {
            FUNC: lambda m: FORMATTING,
        },
    },
    EDITOR_REV: {
        ACCEPT: {
            FUNC: lambda m: COPY_EDIT,
        },
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda m: PUBLISHED,
        },
    },
    PUBLISHED: {
    },
    REJECTED: {
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state, action, manuscript) -> str:
    if curr_state not in STATE_TABLE:
            raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
            raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def main():
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANU))


if __name__ == '__main__':
    main()