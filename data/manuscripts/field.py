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


TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'
AUTHOR_DISP_NM = 'Author'
REFEREES_DISP_NM = 'Referees'
AUTHOR_EMAIL_DISP_NM = 'Author Email'
STATE_DISP_NM = 'State'
TEXT_DISP_NM = 'Text'
EDITOR_DISP_NM = 'Editor'
ABSTRACT_DISP_NM = 'Abstract'
HISTORY_DISP_NM = 'History'




FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
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