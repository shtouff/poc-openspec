from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

from flask import Flask, jsonify
from flask.views import MethodView
from flask_restplus import Api, abort, Resource, fields
from flask_cors import CORS

from marshmallow import Schema, fields as ma_fields


app = Flask(__name__)
api = Api(app, version='1.0', title='UserMVC API', description='A simple UserMVC API', doc='/test/')
CORS(app)


class UserDAO:
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


# Create an APISpec
spec = APISpec(
    title='MA Swagger UserAPI',
    version='1.0.0',
    openapi_version='2.0',
    plugins=(
        FlaskPlugin(),
        MarshmallowPlugin(),
    ),
)


class UserSchema(Schema):
    id = ma_fields.Integer()
    name = ma_fields.String()


class MaUserListResource(MethodView):
    def get(self):
        """Gist view
        ---
        responses:
            200:
                schema:
                    $ref: '#/definitions/User'
        """
        result = UserSchema().dump(DAO.users, many=True).data
        response = jsonify(result)
        return response


@app.route('/maswagger.json')
def maswagger():
    return jsonify(spec.to_dict())


spec.definition('User', schema=UserSchema)
method_view = MaUserListResource.as_view('mauser')
app.add_url_rule("/mauser", view_func=method_view)
with app.test_request_context():
    spec.add_path(view=method_view)


