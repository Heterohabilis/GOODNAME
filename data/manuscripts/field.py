TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
REFEREES = 'referees'
AUTHOR_EMAIL = 'author_email'
STATE = 'state'
TEXT = 'text'
EDITOR = 'editor'
ABSTRACT = 'abstract'
HISTORY = 'history'


TITLE_DISP_NM = TITLE
AUTHOR_DISP_NM = AUTHOR_EMAIL
REFEREES_DISP_NM = REFEREES
AUTHOR_EMAIL_DISP_NM = AUTHOR_EMAIL
STATE_DISP_NM = STATE
TEXT_DISP_NM = TEXT
EDITOR_DISP_NM = EDITOR
ABSTRACT_DISP_NM = ABSTRACT
HISTORY_DISP_NM = HISTORY




FIELDS = {
    TITLE: {
        DISP_NAME: TITLE_DISP_NM,
    },
    AUTHOR: {
        DISP_NAME: AUTHOR_DISP_NM,
    },
    REFEREES: {
        DISP_NAME: REFEREES_DISP_NM,
    },
    AUTHOR_EMAIL: {
        DISP_NAME: AUTHOR_EMAIL_DISP_NM,
    },
    STATE: {
        DISP_NAME: STATE_DISP_NM,
    },
    TEXT: {
        DISP_NAME: TEXT_DISP_NM,
    },
    EDITOR: {
        DISP_NAME: EDITOR_DISP_NM,
    },
    ABSTRACT: {
        DISP_NAME: ABSTRACT_DISP_NM,
    },
    HISTORY: {
        DISP_NAME: HISTORY_DISP_NM,
    },
}




def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm, '')
    return fld[DISP_NAME]



def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()