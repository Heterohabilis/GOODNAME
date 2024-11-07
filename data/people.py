import re

import data.roles as rls

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
        ROLES: [rls.AUTHOR_CODE],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL
    },
    DEL_EMAIL: {
        NAME: 'Cybercricetus',
        ROLES: [rls.CE_CODE],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    }
}


CHAR_OR_DIGIT = '[A-Za-z0-9]'
UNDERSCORE_DASH_DOT = '[-_.]'
CHAR = '[A-Za-z]'


def is_valid_email(addr: str) -> bool:
    prefix_pattern = f"{CHAR_OR_DIGIT}+{UNDERSCORE_DASH_DOT}?{CHAR_OR_DIGIT}+"
    domain_pattern = f"@{CHAR_OR_DIGIT}+[-]?{CHAR_OR_DIGIT}+[.]{CHAR}{{2,}}"
    pattern = f"^{prefix_pattern}{domain_pattern}$"
    return re.match(pattern, addr)


def read():
    people = people_dict
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
    """
    return people_dict.get(email)


def delete_person(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str = None, roles: list = None) -> bool:
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def create_person(name: str, affiliation: str, email: str, role: str):
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    if is_valid_person(name, affiliation, email, role=role):
        roles = []
        if role:
            roles.append(role)
        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: roles}
        return email


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


MH_FIELDS = [NAME, AFFILIATION]


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


def update(name: str, affiliation: str, email: str, roles: list):
    if email not in people_dict:
        raise ValueError(f'Updating non-existent person: {email=}')
    if is_valid_person(name, affiliation, email, roles=roles):
        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: roles}
        return email


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS
