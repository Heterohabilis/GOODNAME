import re

MIN_USER_NAME_LEN = 2
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'zl4490@nyu.edu'
DEL_EMAIL = 'del@nyu.edu'

people_dict = {
    TEST_EMAIL: {
        NAME: 'Elaine Li',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL
    },
    DEL_EMAIL: {
        NAME: 'Cybercricetus',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    }
}


CHAR_OR_DIGIT = '[A-Za-z0-9]'


def is_valid_email(addr: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", addr)


def read():
    people = people_dict
    return people


def delete_person(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def create_people(name: str, affiliation: str, email: str, role: str):
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                          EMAIL: email, ROLES: role}


def get_person(_id):
    people = read()
    if _id in people:
        return people[_id]
    else:
        return None


def set_affiliation(_id, affiliation: str) -> str:
    people = read()
    if _id in people:
        people[_id][AFFILIATION] = affiliation
        return people[_id][AFFILIATION]
    else:
        return None
