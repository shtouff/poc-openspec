from flask import Flask, g
from flask_apispec import marshal_with, use_kwargs, MethodResource, FlaskApiSpec
from flask_cors import CORS

from marshmallow import Schema, fields as ma_fields

from decorators import login_required
from models import UserDAO


DAO = UserDAO()
DAO.create({'name': 'remi'})
DAO.create({'name': 'caro'})

app = Flask(__name__)
CORS(app)

"""
### flask_apispec implementation
"""


def route(app, spec, *urls, **kwargs):
    """
    A `route` decorator to simulate what other frameworks do
    """
    def wrapper(cls):
        methods = ['get', 'post', 'put', 'delete']
        implemented_methods = []

        for method in methods:
            if hasattr(cls, method):
                implemented_methods.append(method)

        for url in urls:
            # craft a name for the view, based on the class name
            name = cls.__name__.lower()
            app.add_url_rule(url, view_func=cls.as_view(name), methods=implemented_methods)

        spec.register(cls)

        return cls
    return wrapper


spec = FlaskApiSpec(app)


class UserSchema(Schema):
    id = ma_fields.Integer()
    name = ma_fields.String()

    class Meta:
        strict = True


class LoginSchema(Schema):
    logged_user = ma_fields.String()


@route(app, spec, '/user')
class UserListResource(MethodResource):
    @marshal_with(UserSchema(many=True))
    def get(self):
        return DAO.users

    @use_kwargs(UserSchema)
    @marshal_with(UserSchema)
    def post(self, **kwargs):
        user = DAO.create(kwargs)
        return user, 201


@route(app, spec, '/user/<int:id>')
class UserResource(MethodResource):
    @use_kwargs(UserSchema)
    @marshal_with(UserSchema)
    def put(self, id, **kwargs):
        user = DAO.get(id)
        user.update(kwargs)
        return user


@route(app, spec, '/protected')
class ProtectedResource(MethodResource):
    @login_required
    @marshal_with(LoginSchema)
    def get(self):
        return {'logged_user': g.logged_user}
