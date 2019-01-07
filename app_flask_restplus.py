from flask import Flask, g
from flask_restplus import Api, Resource, fields
from flask_cors import CORS

from decorators import login_required
from models import UserDAO

DAO = UserDAO()
DAO.create({'name': 'remi'})
DAO.create({'name': 'caro'})

app = Flask(__name__)
CORS(app)

"""
### flask_restplus implementation

"""
api = Api(app, version='1.0', title='UserMVC API', description='A simple UserMVC API', doc='/test/')


user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='The user name')
})


@api.route('/user')
class UserListResource(Resource):
    '''Shows a list of all users, and lets you POST to add new users'''
    @api.doc('list_users')
    @api.marshal_list_with(user)
    def get(self):
        return DAO.users, 200

    @api.doc('create_user')
    @api.expect(user)
    @api.marshal_with(user, code=201)
    def post(self):
        return DAO.create(api.payload), 201


@api.route('/user/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user identifier')
class UserResource(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc('get_user')
    @api.marshal_with(user)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    def delete(self, id):
        '''Delete a user given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(user)
    @api.marshal_with(user)
    def put(self, id):
        '''Update a user given its identifier'''
        return DAO.update(id, api.payload)


login = api.model('Login', {
    'logged_user': fields.String(required=True, description='The logged-in user')
})


@api.route('/protected')
class ProtectedResource(Resource):
    @api.marshal_with(login)
    @login_required
    def get(self):
        return {'logged_user': g.logged_user}

