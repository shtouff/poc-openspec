from flask import Flask
from flask_restplus import Api, abort, Resource, fields
from flask_cors import CORS

app = Flask(__name__)
api = Api(app, version='1.0', title='UserMVC API', description='A simple UserMVC API', doc='/test/')
CORS(app)


class UserDAO(object):
    def __init__(self):
        self.counter = 0
        self.users = []

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        user = data
        user['id'] = self.counter = self.counter + 1
        self.users.append(user)
        return user

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)


DAO = UserDAO()
DAO.create({'name': 'remi'})
DAO.create({'name': 'caro'})


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
