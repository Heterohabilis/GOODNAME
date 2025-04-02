ROLES = {
    'AU': 'Author',
    'ED': 'Editor',
    'ME': 'Managing Editor',
    'CE': 'Copy Editor',
    'RE': 'Referee',
}


ACTION = {
            "SUBMITTED": ["ASSIGN_REF", "REJECT", "WITHDRAW"],
            "IN_REF_REV": ["ACCEPT", "REJECT", "ACCEPT_WITH_REVISIONS", "SUBMIT_REVIEW", "ASSIGN_REF", "DELETE_REF", "WITHDRAW"],
            "AUTHOR_REVISION": ["DONE"],
            "COPY_EDIT": ["DONE", "WITHDRAW"],
            "AUTHOR_REV": ["DONE", "WITHDRAW"],
            "EDITOR_REV": ["ACCEPT"],
            "FORMATTING": ["DONE"],
            "PUBLISHED": [],
            "REJECTED": ["WITHDRAW"],
            "WITHDRAWN": ["WITHDRAW"]
        }
