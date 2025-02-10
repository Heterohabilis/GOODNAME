from bson import ObjectId

import data.db_connect as dbc

import data.manuscripts.field as flds

MANUSCRIPT_COLLECT = 'manuscripts'

client = dbc.connect_db()

AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'  #
EDITOR_REV = 'EDR'
AUTHOR_REVISION = 'ARV'
FORMATTING = 'FMT'
PUBLISHED = 'PUB'
ACTION = 'ACT'
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
    WITHDRAWN,  #
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
WITHDRAW = 'WIT'  #
REMOVE_REF = 'RRF'
SUBMIT_REVIEW = 'SBR'
ACCEPT_WITH_REVISIONS = 'AWR'

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,  #
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
MANU = 'manu'


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    print(extra)
    manu[flds.REFEREES].append(referee)
    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(referee)
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
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
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


def handle_action(_id, curr_state, action, **kwargs) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


ID = "_id"
CURR_STATE = "curr_state"
REFEREE = "referee"


def create_query(_id: str) -> dict:
    return {ID: ObjectId(_id)}


def read_one(_id: str) -> dict:
    id_dic = create_query(_id)
    return dbc.read_one(MANUSCRIPT_COLLECT, id_dic)


def exists(_id: str):
    return read_one(_id) is not None


def read():
    text = dbc.read(MANUSCRIPT_COLLECT, dbc.SE_DB, True)
    return text


def delete(_id: str):
    return dbc.delete(MANUSCRIPT_COLLECT, create_query(_id))


def create(title: str, author: str, author_email: str, text: str, abstract: str, editor: str):
    new_item = {flds.TITLE: title, flds.AUTHOR: author, flds.AUTHOR_EMAIL: author_email,
                flds.STATE: SUBMITTED, flds.REFEREES: [], flds.TEXT: text,
                flds.ABSTRACT: abstract, flds.HISTORY: [SUBMITTED], flds.EDITOR: editor}
    result = dbc.create(MANUSCRIPT_COLLECT, new_item)
    return str(result.inserted_id)


def update(_id: str, title: str, author: str, author_email: str, text: str, abstract: str, editor: str):
    if not exists(_id):
        raise ValueError('Manuscript not exist')
    update_dict = {flds.TITLE: title, flds.AUTHOR: author, flds.AUTHOR_EMAIL: author_email,
                   flds.STATE: SUBMITTED, flds.REFEREES: [], flds.TEXT: text,
                   flds.ABSTRACT: abstract, flds.HISTORY: [SUBMITTED], flds.EDITOR: editor}
    dbc.update(MANUSCRIPT_COLLECT, create_query(_id), update_dict)
    return _id


# def update_state(_id: str, curr_state: str, action: str, **kwargs):
#     manuscript = read_one(_id)
#     if not exists(_id):
#         raise ValueError(f"Manuscript not exist")
#     curr_state = manuscript[flds.STATE]
#     if action not in get_valid_actions_by_state(curr_state):
#         raise ValueError(f"Action '{action}' is not valid for the current state '{curr_state}'")
#
#     new_state = handle_action(curr_state, action, manu=manuscript, **kwargs)
#     update_dict = {
#         flds.STATE: new_state,
#         flds.HISTORY: manuscript[flds.HISTORY] + [new_state],
#     }
#     dbc.update(MANUSCRIPT_COLLECT, create_query(_id), update_dict)
#     return new_state


def main():
    print(handle_action(SUBMITTED, ASSIGN_REF,
                        manu=SAMPLE_MANU, ref='Jack'))
    print(handle_action(SUBMITTED, WITHDRAW, manu=SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, manu=SAMPLE_MANU))

    print(handle_action(IN_REF_REV, ASSIGN_REF, manu=SAMPLE_MANU,
                        ref='Jill', extra='Extra!'))
    print(handle_action(IN_REF_REV, DELETE_REF, manu=SAMPLE_MANU,
                        ref='Jill'))
    print(handle_action(IN_REF_REV, DELETE_REF, manu=SAMPLE_MANU,
                        ref='Jack'))
    print(handle_action(IN_REF_REV, ACCEPT, manu=SAMPLE_MANU))
    print(handle_action(IN_REF_REV, ACCEPT_WITH_REVISIONS, manu=SAMPLE_MANU))
    print(handle_action(IN_REF_REV, SUBMIT_REVIEW, manu=SAMPLE_MANU))
    print(handle_action(IN_REF_REV, WITHDRAW, manu=SAMPLE_MANU))

    print(handle_action(AUTHOR_REVISION, DONE, manu=SAMPLE_MANU))
    print(handle_action(EDITOR_REV, ACCEPT, manu=SAMPLE_MANU))
    print(handle_action(COPY_EDIT, DONE, manu=SAMPLE_MANU))
    print(handle_action(AUTHOR_REV, DONE, manu=SAMPLE_MANU))
    print(handle_action(FORMATTING, DONE, manu=SAMPLE_MANU))


if __name__ == '__main__':
    main()
    #idx = create("a", "b", "c", "d", "e", "g")
    #delete('675e6b4f7a057d0f581d3dee')
    print(read_one('675e6b4f7a057d0f581d3dee'))
