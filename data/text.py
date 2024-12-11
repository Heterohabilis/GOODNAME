"""
This module interfaces to our user data.
"""
import data.db_connect as dbc

# fields
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEXT_COLLECT = 'text'

TEST_title = 'HomePage'
DEL_title = 'DeletePage'
SUBM_title = 'SubmissonsPage'

# text_dict = {
#     TEST_title: {
#         TITLE: 'Home Page',
#         TEXT: 'This is a journal about building API servers.',
#     },
#     DEL_title: {
#         TITLE: 'Home Page',
#         TEXT: 'This is a text to delete.',
#     },
#     SUBM_title: {
#         TITLE: 'Submissions Page',
#         TEXT: 'All submissions must be original work in Word format.',
#     }
# }

client = dbc.connect_db()
print(f'{client=}')


def exists(title):
    return read_one(title) is not None


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users titleed on user email.
        - Each user email must be the title for another dictionary.
    """
    text = dbc.read_dict(TEXT_COLLECT, TITLE)
    return text


def read_one(title: str) -> dict:
    # This should take a title and return the page dictionary
    # for that title. Return an empty dictionary of title not found.
    return dbc.read_one(TEXT_COLLECT, {TITLE: title})


def delete(title):
    return dbc.delete(TEXT_COLLECT, {TITLE: title})


def create(title, text, email=None):
    if exists(title):
        raise ValueError('Page already exists!')
    if email:
        new_page = {TITLE: title, TEXT: text, EMAIL: email}
    else:
        new_page = {TITLE: title, TEXT: text}
    print(f'{new_page=}')
    return dbc.create(TEXT_COLLECT, new_page)


def update(title, text, email=None):
    if not exists(title):
        raise ValueError('Page does not exist!')
    dbc.update(TEXT_COLLECT, {TITLE: title},
               {TITLE: title, TEXT: text, EMAIL: email})
    return title


def main():
    print(read())


if __name__ == '__main__':
    main()
