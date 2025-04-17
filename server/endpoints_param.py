ENDPOINT_PARAMS = {
    '/people/<email> [PUT]':       ['name', 'affiliation', 'roles'],
    '/people/create [PUT]':        ['name', 'email', 'affiliation', 'roles'],
    '/people/set_affiliation [PUT]': ['email', 'affiliation'],
    '/text/<_id> [PUT]':           ['text', 'email'],
    '/text/create [PUT]':          ['title', 'text', 'email'],
    '/manuscript/<_id> [PUT]':
        ['title', 'author', 'author_email', 'text', 'abstract', 'editor'],
    '/manuscript/create [PUT]':
        ['title', 'author', 'author_email', 'text', 'abstract', 'editor'],
    '/manuscript/<_id>/update_state [PUT]': ['action', 'referee (optional)'],
    '/manuscript/receive_action [PUT]':
        ['curr_state', 'action', 'referee (optional)'],
    '/login [PUT]':                ['username', 'password'],
}
