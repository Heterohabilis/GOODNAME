import data.db_connect as dbc
import data.manuscripts.field as flds


MANUSCRIPT_COLLECT = 'manuscripts'

client = dbc.connect_db()


AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'    #
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
    WITHDRAWN,      #
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
DELETE_REF = 'DRF'  #
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'    #
REMOVE_REF = 'RRF'
SUBMIT_REVIEW = 'SBR'
ACCEPT_WITH_REVISIONS = 'AWR'

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,     #
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


#---------------------------------------------------------------
def assign_ref(manu: dict, ref: str, extra=None) -> str:
    print(extra)
    manu[flds.REFEREES].append(ref)
    return IN_REF_REV


def delete_ref(manu: dict, ref: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(ref)
    if len(manu[flds.REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED
#--------------------------------------------------------------------

FUNC = 'f'

#----------------------------------------------
COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}
#----------------------------------------------

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,  #
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,  #
        },
        **COMMON_ACTIONS,  #
    },
    IN_REF_REV: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        ACCEPT_WITH_REVISIONS: {
            FUNC: lambda **kwargs: AUTHOR_REVISION,
        },
        SUBMIT_REVIEW: {
            FUNC: lambda **kwargs: IN_REF_REV,
        },
        # ------------------------------------------
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISION: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REV,
        },
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REV,  #
        },
        **COMMON_ACTIONS,  #
    },
    AUTHOR_REV: {
        **COMMON_ACTIONS,  #
    },
    EDITOR_REV: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
    },
    PUBLISHED: {},
    REJECTED: {
        **COMMON_ACTIONS,  #
    },
    # ----------------------------------
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
    # ----------------------------------
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state, action, **kwargs) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


# def read():
#     """
#     Our contract:
#         - No arguments.
#         - Returns a dictionary of manuscripts.
#         - Each user email must be the title for another dictionary.
#     """
#     text = dbc.read_dict(MANUSCRIPT_COLLECT, TITLE)
#     return text
#
#
# def read_one(title: str) -> dict:
#     return dbc.read_one(MANUSCRIPT_COLLECT, {TITLE: title})
#
#
# def exists(title):
#     return read_one(title) is not None

def main():
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANU))


if __name__ == '__main__':
    main()