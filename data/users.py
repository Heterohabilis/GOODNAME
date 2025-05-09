"""
This module interfaces to our user data.
"""
import data.db_connect as dbc

LEVEL = 'level'
MIN_USER_NAME_LEN = 2

client = dbc.connect_db()
USERS_COLLECT = 'users'
USERNAME = 'username'
PASSWORD = 'password'
NAME = 'name'
AFFILIATION = 'affiliation'


def exists(username):
    """
    Check if a user exists in the database.
    """
    return dbc.read_one(collection=USERS_COLLECT,
                        filt={USERNAME: username}) is not None


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    return dbc.read_dict(USERS_COLLECT, USERNAME)


# editor=1, author=0
def add_user(username, password, name, affiliation, level=0):
    if len(username) < MIN_USER_NAME_LEN:
        return {"error": f"Username must be at least "
                         f"{MIN_USER_NAME_LEN} characters long."}

    if exists(username):
        return {"error": "User already exists."}

    if level not in [0, 1]:
        return {"error": "Invalid role specified. Must be 0 or 1."}

    dbc.create(collection=USERS_COLLECT,
               doc={USERNAME: username, PASSWORD: password,
                    LEVEL: level, NAME: name, AFFILIATION: affiliation})
    """
    try:
        ppl.create(name=name, affiliation=affiliation,
                   email=username, role=role_name)
    except ValueError as e:
        return {"error": str(e)}
    """
    return {"message": f"User '{username}' registered successfully.",
            "user": {"username": username, LEVEL: level}}


def delete_user(username):
    if not exists(username):
        return {"error": "User not found."}

    dbc.delete(collection=USERS_COLLECT, filt={USERNAME: username})
    return {"message": f"User '{username}' deleted successfully."}


def update_user(username, password, name, affiliation, level):
    if not exists(username):
        return {"error": "User not found."}

    dbc.update(collection=USERS_COLLECT, filters={USERNAME: username},
               update_dict={LEVEL: level, PASSWORD: password,
                            NAME: name, AFFILIATION: affiliation})
    return {"message": f"User '{username}' updated successfully.",
            "user": {USERNAME: username, PASSWORD: password,
                     LEVEL: level, NAME: name, AFFILIATION: affiliation}}


def verify_password(username, password):
    user = dbc.read_one(collection=USERS_COLLECT, filt={USERNAME: username})
    if user and PASSWORD in user:
        return user[PASSWORD] == password
    return False
