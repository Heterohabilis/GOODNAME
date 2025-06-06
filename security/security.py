from functools import wraps
import data.people as ppl
import data.roles as rl
import data.db_connect as dbc
from data.db_connect import create, fetch_all_as_dict, SE_DB

"""
Our record format to meet our requirements (see security.md) will be:

{
    feature_name1: {
        create: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        read: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        update: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        delete: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
    },
    feature_name2: # etc.
}
"""

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'
LOGIN_KEY = 'login_key'
IP_ADDR = 'ip_address'
DUAL_FACTOR = 'dual_factor'


# Features:
PEOPLE = 'people'
TEXTS = 'texts'
MANUSCRIPT = 'manuscript'
BAD_FEATURE = 'baaaad feature'

ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'  #
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'  #
REMOVE_REF = 'RRF'
SUBMIT_REVIEW = 'SBR'
ACCEPT_WITH_REVISIONS = 'AWR'
LEVEL_ADMIN = "level_admin"
LEVEL = "level"
IS_ADMIN = 1

PEOPLE_MISSING_ACTION = READ
GOOD_USER_ID = 'elaine@nyu.edu'

security_recs = None

PEOPLE_CHANGE_PERMISSIONS = {
    # USER_LIST: [GOOD_USER_ID],
    CHECKS: {
        LEVEL_ADMIN: True,
    },
}

TEXTS_CHANGE_PERMISSIONS = {
    CHECKS: {
        LEVEL_ADMIN: True,
    },
}

MANUSCRIPT_CHANGE_PERMISSIONS = {
    CHECKS: {
        LEVEL_ADMIN: True,
    },
}

'''

# These will come from the DB soon:
TEST_RECS = {
    PEOPLE: {
        CREATE: PEOPLE_CHANGE_PERMISSIONS,
        DELETE: PEOPLE_CHANGE_PERMISSIONS,
        UPDATE: PEOPLE_CHANGE_PERMISSIONS,
    },
    TEXTS: {
        CREATE: TEXTS_CHANGE_PERMISSIONS,
        UPDATE: TEXTS_CHANGE_PERMISSIONS,
        DELETE: TEXTS_CHANGE_PERMISSIONS,
    },
    MANUSCRIPT: {
        ACCEPT: MANUSCRIPT_CHANGE_PERMISSIONS,
        ASSIGN_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
        DELETE_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
        DONE: MANUSCRIPT_CHANGE_PERMISSIONS,
        REJECT: MANUSCRIPT_CHANGE_PERMISSIONS,
        REMOVE_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
        SUBMIT_REVIEW: MANUSCRIPT_CHANGE_PERMISSIONS,
        WITHDRAW: MANUSCRIPT_CHANGE_PERMISSIONS,
        ACCEPT_WITH_REVISIONS: MANUSCRIPT_CHANGE_PERMISSIONS,
    },

    BAD_FEATURE: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                'Bad check': True,
            },
        },
    },
}
'''


def is_valid_key(user_id: str, login_key: str):
    """
    This is just a mock of the real is_valid_key() we'll write later.
    """
    return True


def check_level_admin(user_id: str, **kwargs) -> bool:
    user = ppl.read_one(user_id)
    if user:
        roles = user.get(ppl.ROLES, [])
        if rl.AUTHOR_CODE in roles:
            return False
        return True
    else:
        return False


def check_login(user_id: str, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key(user_id, kwargs[LOGIN_KEY])


def check_ip(user_id: str, **kwargs):
    if IP_ADDR not in kwargs:
        return False
    # we would check user's IP address here
    return True


def get_user_roles(user_id: str) -> list:
    """
    Placeholder function to get user roles from the database or another source.
    Replace this with your actual implementation.
    """

    if user_id == "elaine@nyu.edu":
        return ["ED", "AU"]
    else:
        return ["AU"]


def check_role(user_id: str, required_role: str, **kwargs):
    user_roles = get_user_roles(user_id)
    return required_role in user_roles


def dual_factor(user_id: str, **kwargs):
    return True


CHECK_FUNCS = {
    LOGIN: check_login,
    IP_ADDR: check_ip,
    DUAL_FACTOR: dual_factor,
    LEVEL_ADMIN: check_level_admin,
}


def read() -> dict:
    global security_recs
    # Replace the hard-coded test records with database fetch
    connect_db()
    security_recs = fetch_all_as_dict('feature', COLLECT_NAME, SE_DB)
    if not security_recs:  # If the collection is empty, initialize it
        initialize_security_records()
        security_recs = fetch_all_as_dict('feature', COLLECT_NAME, SE_DB)
    return security_recs


def initialize_security_records():
    connect_db()

    records = [
        {
            'feature': PEOPLE,
            'permissions': {
                CREATE: PEOPLE_CHANGE_PERMISSIONS,
                DELETE: PEOPLE_CHANGE_PERMISSIONS,
                UPDATE: PEOPLE_CHANGE_PERMISSIONS,
            }
        },
        {
            'feature': TEXTS,
            'permissions': {
                CREATE: TEXTS_CHANGE_PERMISSIONS,
                UPDATE: TEXTS_CHANGE_PERMISSIONS,
                DELETE: TEXTS_CHANGE_PERMISSIONS,
            }
        },
        {
            'feature': MANUSCRIPT,
            'permissions': {
                ACCEPT: MANUSCRIPT_CHANGE_PERMISSIONS,
                ASSIGN_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
                DELETE_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
                DONE: MANUSCRIPT_CHANGE_PERMISSIONS,
                REJECT: MANUSCRIPT_CHANGE_PERMISSIONS,
                REMOVE_REF: MANUSCRIPT_CHANGE_PERMISSIONS,
                SUBMIT_REVIEW: MANUSCRIPT_CHANGE_PERMISSIONS,
                WITHDRAW: MANUSCRIPT_CHANGE_PERMISSIONS,
                ACCEPT_WITH_REVISIONS: MANUSCRIPT_CHANGE_PERMISSIONS,
            }
        },
        {
            'feature': BAD_FEATURE,
            'permissions': {
                CREATE: {
                    USER_LIST: [GOOD_USER_ID],
                    CHECKS: {
                        'Bad check': True,
                    },
                },
            }
        }
    ]

    for record in records:
        create(COLLECT_NAME, record)


def connect_db():
    return dbc.connect_db()


def needs_recs(fn):
    """
    Should be used to decorate any function that directly accesses sec recs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]['permissions']
    else:
        return None


@needs_recs
def is_permitted(feature_name: str, action: str,
                 user_id: str, **kwargs) -> bool:
    prot = read_feature(feature_name)
    # print(feature_name, action, user_id, kwargs, prot, sep=';')
    if prot is None:
        return True
    if action not in prot:
        return True
    if USER_LIST in prot[action]:
        if user_id not in prot[action][USER_LIST]:
            return False
    if CHECKS not in prot[action]:
        return True
    for check in prot[action][CHECKS]:
        if check not in CHECK_FUNCS:
            raise ValueError(
                f'Bad check passed to is_permitted: {check}'
            )
        if not CHECK_FUNCS[check](user_id, **kwargs):
            return False
    return True


def main():
    connect_db()


if __name__ == '__main__':
    main()
