"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace     # fields
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl
import data.text as tx
import data.manuscripts.query as qy
import data.manuscripts.action_form as af
import data.role_form as rf
# import examples.form_filler as ff
import examples.form as fm
import data.users as us
from server.endpoints_param import ENDPOINT_PARAMS


# import werkzeug.exceptions as wz

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'

# My ep and resp
CRICETUS_EP = '/cricetus'
CRICETUS_RESP = 'cybercricetus'

# Journal Stuffs
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'Nostra Repositoria'
EDITOR_RESP = 'Editor'
EDITOR = 'Cybercricetus xm2204@nyu.edu'
DATE_RESP = 'Date'
DATE = '2024-10-01'
PEOPLE_EP = '/people'
TEXT_EP = '/text'
MANU_EP = '/manuscript'
LOGIN_EP = '/login'
REGISTER_EP = "/register"
USER_EP = "/users"

MESSAGE = "Message"
RETURN = 'return'
NAME = 'name'


# Journal Retrieval class
@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title.
    """

    def get(self):
        """
        Retrieve the journal title.
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
        }


# My class
@api.route(CRICETUS_EP)
class HelloCricetus(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """

    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {CRICETUS_RESP: 'Ich kein bin ein Hamster...'}


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """

    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """

    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self):
        """
        Retrieve the journal people.
        """
        return ppl.read()


PEOPLE_UPDATE_FLDS = api.model('UpdatePeopleEntry', {
    ppl.NAME: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String),
})


@api.route(f'{PEOPLE_EP}/<email>')
class Person(Resource):
    """
    This class handles creating, reading, updating and deleting a person.
    """
    def get(self, email):
        """
        Retrieve the journal person.
        """
        person = ppl.read_one(email)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {email}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, email):
        """
        Delete the journal person.
        """
        ret = ppl.delete(email)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {email}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_UPDATE_FLDS)
    def put(self, email):
        """
        Update the journal person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            role = request.json.get(ppl.ROLES)
            print(f'{role=}')
            ret = ppl.update(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
            RETURN: ret,
        }


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/create')
class PeopleCreate(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


AFF_SET_FLDS = api.model('AffiliationSetEntry', {
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
})


@api.route(f'{PEOPLE_EP}/set_affiliation')
class SetAffiliation(Resource):
    """
    This endpoint is for setting affiliation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(AFF_SET_FLDS)
    def put(self):
        try:
            _id = request.json.get(ppl.EMAIL)
            affiliation = request.json.get(ppl.AFFILIATION)
            ret = ppl.set_affiliation(_id, affiliation)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not set affiliation: '
                                   f'{err=}')
        if ret:
            return {
                MESSAGE: 'Affilation set!',
                RETURN: f'New Affiliation: {ret}',
            }
        else:
            return {
                MESSAGE: 'Cannot find such people!',
                RETURN: f'Value: {ret}'
            }


@api.route(TEXT_EP)
class Texts(Resource):
    """
    This class handles creating, reading, updating and deleting text.
    """
    def get(self):
        return tx.read()


TEXT_UPDATE_FLDS = api.model('UpdateTextEntry', {
    tx.TEXT: fields.String,
    tx.EMAIL: fields.String,
})


@api.route(f'{TEXT_EP}/<_id>')
class Text(Resource):
    """
    This class handles creating, reading, updating and deleting text.
    """
    def get(self, _id):
        text = tx.read_one(_id)
        if text:
            return text
        else:
            raise wz.NotFound(f'No such record: {_id}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such text.')
    def delete(self, _id):
        ret = tx.delete(_id)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such text: {_id}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_UPDATE_FLDS)
    def put(self, _id):
        try:
            title = _id
            text = request.json.get(tx.TEXT)
            email = request.json.get(tx.EMAIL)
            ret = tx.update(title, text, email)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Text updated!',
            RETURN: ret,
        }


TEXT_CREATE_FLDS = api.model('AddNewTextEntry', {
    tx.TITLE: fields.String,
    tx.TEXT: fields.String,
    tx.EMAIL: fields.String,
})


@api.route(f'{TEXT_EP}/create')
class TextCreate(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_CREATE_FLDS)
    def put(self):
        try:
            title = request.json.get(tx.TITLE)
            text = request.json.get(tx.TEXT)
            email = request.json.get(tx.EMAIL)
            ret = tx.create(title, text, email)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Text added!',
            RETURN: ret,
        }


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}


@api.route(MANU_EP)
class Manuscripts(Resource):
    def get(self):
        return qy.read()


MANU_UPDATE_FLDS = api.model('UpdateManuEntry', {
    qy.flds.TITLE: fields.String,
    qy.flds.AUTHOR: fields.String,
    qy.flds.AUTHOR_EMAIL: fields.String,
    qy.flds.TEXT: fields.String,
    qy.flds.ABSTRACT: fields.String,
    qy.flds.EDITOR: fields.String,
})


@api.route(f'{MANU_EP}/<_id>')
class Manuscript(Resource):
    """
    This class handles creating, reading, updating and deleting a manuscript.
    """
    def get(self, _id):
        manuscript = qy.read_one(_id)
        if manuscript:
            return manuscript
        else:
            raise wz.NotFound(f'No such record: {_id}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such text.')
    def delete(self, _id):
        ret = qy.delete(_id)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such manuscript: {_id}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_UPDATE_FLDS)
    def put(self, _id):
        try:
            title = request.json.get(qy.flds.TITLE)
            author = request.json.get(qy.flds.AUTHOR)
            author_email = request.json.get(qy.flds.AUTHOR_EMAIL)
            text = request.json.get(qy.flds.TEXT)
            abstract = request.json.get(qy.flds.ABSTRACT)
            editor = request.json.get(qy.flds.EDITOR)
            ret = qy.update(
                _id, title, author, author_email, text, abstract, editor
            )
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript updated!',
            RETURN: ret,
        }


MANU_CREATE_FLDS = api.model('CreateManuEntry', {
    qy.flds.TITLE: fields.String,
    qy.flds.AUTHOR: fields.String,
    qy.flds.AUTHOR_EMAIL: fields.String,
    qy.flds.TEXT: fields.String,
    qy.flds.ABSTRACT: fields.String,
    qy.flds.EDITOR: fields.String,
})


@api.route(f'{MANU_EP}/create')
class ManuCreate(Resource):
    """
    This class handles creating a manuscript
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        try:
            title = request.json.get(qy.flds.TITLE)
            author = request.json.get(qy.flds.AUTHOR)
            author_email = request.json.get(qy.flds.AUTHOR_EMAIL)
            text = request.json.get(qy.flds.TEXT)
            abstract = request.json.get(qy.flds.ABSTRACT)
            editor = request.json.get(qy.flds.EDITOR)
            ret = qy.create(
                title, author, author_email, text, abstract, editor
            )
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript added!',
            RETURN: ret,
        }


UPDATE_ENTRY = api.model('UpdateActionEntry', {
    qy.ACTION: fields.String,
    qy.REFEREE: fields.String,
})


@api.route(f'{MANU_EP}/<_id>/update_state')
@api.expect(UPDATE_ENTRY)
class ManuUpdateState(Resource):
    def put(self, _id):
        try:
            action = request.json.get(qy.ACTION)
            if action == qy.ASSIGN_REF or qy.DELETE_REF:
                ref = request.json.get(qy.REFEREE)
                ret = qy.update_state(_id, action, referee=ref)
            else:
                ret = qy.update_state(_id, action)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update state: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript state updated!',
            RETURN: ret,
        }


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    qy.ID: fields.String,
    qy.CURR_STATE: fields.String,
    qy.ACTION: fields.String,
    qy.REFEREE: fields.String,
})


@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            # manu_id = request.json.get(qy.ID)
            curr_state = request.json.get(qy.CURR_STATE)
            action = request.json.get(qy.ACTION)
            kwargs = {}
            if action == qy.ASSIGN_REF or qy.DELETE_REF:
                kwargs[qy.REFEREE] = request.json.get(qy.REFEREE)

            ret = qy.handle_action(curr_state, action, **kwargs)
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }


@api.route('/roles')
class Roles(Resource):
    """
    This endpoint returns available roles for people.
    """
    def get(self):
        return rf.get_form()


@api.route('/actions')
class Actions(Resource):
    """
    Return all possible manuscript actions grouped by state.
    """
    def get(self):
        return af.get_form()


VALID_USERS = {"elaine@nyu.edu": "password"}
LOGIN_FLDS = api.model('LoginEntry', {
    'username': fields.String,
    'password': fields.String,
})


@api.route(USER_EP)
class Users(Resource):
    """
    This class handles user management.
    """

    def get(self):
        """
        Retrieve all users.
        """
        return us.get_users()


REGISTER_FLDS = api.model('RegisterEntry', {
    'username': fields.String(required=True),
    'level': fields.Integer(default=0),
    'password': fields.String(required=True),
})


@api.route(f'{USER_EP}/<username>')
class User(Resource):
    """
    This class handles user management.
    """

    def get(self, username):
        """
        Retrieve a specific user.
        """
        user = us.get_users().get(username)
        if user:
            return user
        else:
            raise wz.NotFound(f'No such user: {username}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'No such user.')
    def delete(self, username):
        """
        Delete a specific user.
        """
        ret = us.delete_user(username)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such user: {username}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(REGISTER_FLDS)
    def put(self, username):
        """
        Update a specific user.
        """
        try:
            password = request.json.get("password")
            level = request.json.get("level", 0)
            ret = us.update_user(username, password, level)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update user: '
                                   f'{err=}')
        return {
            MESSAGE: 'User updated!',
            RETURN: ret,
        }


@api.route(LOGIN_EP)
class Login(Resource):
    """
    This class handles user login.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Missing required fields')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Invalid credentials')
    @api.expect(LOGIN_FLDS)
    def put(self):
        """
        Authenticate a user based on query parameters.
        """
        try:
            username = request.json.get("username")
            password = request.json.get("password")

            if not username:
                return ({"error": "Username is required."},
                        HTTPStatus.BAD_REQUEST)

            if us.verify_password(username, password):
                return {"message": f"Welcome, {username}!"}, HTTPStatus.OK
            else:
                return ({"error": "Invalid username or password."},
                        HTTPStatus.UNAUTHORIZED)
        except Exception as err:
            raise wz.NotAcceptable(f'Login failed: {err=}')


REGISTER_FLDS = api.model('RegisterEntry', {
    'username': fields.String(required=True),
    'level': fields.Integer(default=0),
    'password': fields.String(required=True),
})


@api.route(REGISTER_EP)
class Register(Resource):
    """
    Endpoint to register a new user.
    """

    @api.expect(REGISTER_FLDS)
    @api.response(HTTPStatus.CREATED, 'User registered')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid data or user exists')
    def post(self):
        try:
            username = request.json.get("username")
            password = request.json.get("password")
            level = request.json.get("level", 0)

            if not username:
                return ({"error": "Username is required."},
                        HTTPStatus.BAD_REQUEST)

            result = us.add_user(username=username,
                                 password=password, level=level)

            if "error" in result:
                return result, HTTPStatus.BAD_REQUEST
            else:
                return result, HTTPStatus.CREATED
        except Exception as err:
            raise wz.NotAcceptable(f'Registration failed: {err=}')


@api.route(f'{LOGIN_EP}/form')
class LoginForm(Resource):
    """
    Return form structure for login.
    """

    def get(self):
        return fm.get_form_descr()


developer_ns = Namespace(
    name='developer',
    description='Developer utilities (hidden)',
    path='/developer'
)


@developer_ns.route('/endpoints')
class DevEndpoints(Resource):
    def get(self):
        """
        Return a sorted list of all active URL rules.
        """
        routes = sorted(rule.rule for rule in app.url_map.iter_rules())
        return {'active_endpoints': routes}


@developer_ns.route('/params')
class DevParams(Resource):
    def get(self):
        """
        returns the parameters of the endpoints
        """
        return {'endpoint_params': ENDPOINT_PARAMS}


api.add_namespace(developer_ns)
