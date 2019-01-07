from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

from flask import Flask, jsonify, g
from flask.views import MethodView

from marshmallow import Schema, fields as ma_fields

from decorators import login_required
from models import UserDAO


DAO = UserDAO()
DAO.create({'name': 'remi'})
DAO.create({'name': 'caro'})

app = Flask(__name__)

"""
### flask + marshmallow + apispec implementation
"""

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
        """User list
        ---
        responses:
            200:
                schema:
                    $ref: '#/definitions/User'
        """
        result = UserSchema().dump(DAO.users, many=True).data
        response = jsonify(result)
        return response


class ProtectedResource(MethodView):
    @login_required
    def get(self):
        return jsonify({'logged_user': g.logged_user})


@app.route('/swagger.json')
def maswagger():
    return jsonify(spec.to_dict())


spec.definition('User', schema=UserSchema)


def add_url_rule_and_spec_path(url, cls):
    method_view = cls.as_view(cls.__name__.lower())
    app.add_url_rule(url, view_func=method_view)

    with app.app_context():
        spec.add_path(view=method_view)


add_url_rule_and_spec_path('/user', MaUserListResource)
add_url_rule_and_spec_path('/protected', ProtectedResource)

