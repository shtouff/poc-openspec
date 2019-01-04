import pytest

from app import app, api


@pytest.fixture(scope='function')
def test_client():
    return app.test_client()


def assert_is_json(response):
    assert hasattr(response, 'json')


def assert_1st_user_is_remi(test_client, url):
    response = test_client.get(url)
    assert_is_json(response)
    assert response.json[0].get('name') == 'remi'


def assert_swagger_is_ok(test_client, url):
    response = test_client.get(url)
    assert_is_json(response)
    print(response.json)
    assert response.json.get('swagger') == '2.0'


def test_flask_restplus(test_client):
    assert_1st_user_is_remi(test_client, '/user')
    assert_swagger_is_ok(test_client, '/swagger.json')


def test_apispec(test_client):
    assert_1st_user_is_remi(test_client, '/mauser')
    assert_swagger_is_ok(test_client, '/maswagger.json')
