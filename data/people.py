MIN_USER_NAME_LEN = 2
NAME = 'name'
ROLES = 'roles'
AFFLIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'zl4490@nyu.edu'

people_dict = {
    TEST_EMAIL: {
        NAME: 'Elaine Li',
        ROLES: [],
        AFFLIATION: 'NYU',
        EMAIL: TEST_EMAIL
    }
}


def get_people():
    people = people_dict
    return people
