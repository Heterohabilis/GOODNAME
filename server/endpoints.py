"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields  # Namespace, fields
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl
import data.text as tx

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

MESSAGE = "Message"
RETURN = 'return'


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


@api.route(f'{PEOPLE_EP}/<_id>')
class Person(Resource):
    """
    This class handles creating, reading, updating and deleting a person.
    """
    def get(self, _id):
        """
        Retrieve the journal person.
        """
        person = ppl.get_person(_id)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {_id}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, _id):
        """
        Delete the journal person.
        """
        ret = ppl.delete_person(_id)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String),
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
            roles = request.json.get(ppl.ROLES)
            if not ppl.is_valid_email(email):
                return {
                    MESSAGE: 'Wrong Email Format',
                    RETURN: None,
                }
            ret = ppl.create_person(name, affiliation, email, roles)
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
class Text(Resource):
    """
    This class handles creating, reading, updating and deleting text.
    """
    def get(self):
        return tx.read()
