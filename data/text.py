"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
DEL_KEY = 'DeletePage'
SUBM_KEY = 'SubmissonsPage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    DEL_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a text to delete.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    }
}


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Return an empty dictionary of key not found.
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def delete(key):
    # This should take a key and delete the page dictionary
    # for that key. Return the key if it was deleted, else None.
    if key in text_dict:
        del text_dict[key]
        return key
    return None


def create(title, text, email=None):
    # This should take a key and create a new page dictionary
    # for that key. Return the key if it was created, else None.
    key = title.replace(' ', '')
    if key in text_dict:
        raise ValueError(f'Adding duplicate {key=}')
    if email:
        text_dict[key] = {TITLE: title, TEXT: text, EMAIL: email}
    else:
        text_dict[key] = {TITLE: title, TEXT: text}
    return key


def update(key, title, text, email=None):
    # This should take a key and update the page dictionary
    # for that key. Return the key if it was updated, else None.
    if key in text_dict:
        if email:
            text_dict[key] = {TITLE: title, TEXT: text, EMAIL: email}
        else:
            text_dict[key] = {TITLE: title, TEXT: text}
        return key
    return None


def main():
    print(read())


if __name__ == '__main__':
    main()
