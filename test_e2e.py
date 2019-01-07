import pytest

from app_flask_restplus import app as app_flask_restplus
from app_ma_apispec import app as app_ma_apispec
from app_flask_apispec import app as app_flask_apispec


def assert_is_json(response):
    assert hasattr(response, 'json')


@pytest.mark.parametrize('test_client,user_list_url', [
    (app_flask_restplus.test_client(), '/user'),
    (app_ma_apispec.test_client(), '/user'),
    (app_flask_apispec.test_client(), '/user'),
])
def test_app(test_client, user_list_url):
    response = test_client.get(user_list_url)
    assert_is_json(response)
    assert response.json[0].get('name') == 'remi'


@pytest.mark.parametrize('test_client,swagger_url', [
    (app_flask_restplus.test_client(), '/swagger.json'),
    (app_ma_apispec.test_client(), '/swagger.json'),
    (app_flask_apispec.test_client(), '/swagger/'),
])
def test_app_swagger(test_client, swagger_url):
    response = test_client.get(swagger_url)
    assert_is_json(response)

    swagger = response.json
    assert swagger.get('swagger') == '2.0'
    assert 'post' in swagger.get('paths', {}).get('/user', {})


@pytest.mark.parametrize('test_client,protected_url', [
    (app_flask_restplus.test_client(), '/protected'),
    (app_ma_apispec.test_client(), '/protected'),
    (app_flask_apispec.test_client(), '/protected'),
])
def test_app_protected(test_client, protected_url):
    response = test_client.get(protected_url)
    assert response.status_code == 401

    response = test_client.get(protected_url, headers={'X-Authenticated-As': 'foo'})
    assert response.status_code == 200

    assert_is_json(response)
    assert response.json.get('logged_user') == 'foo'


@pytest.mark.parametrize('test_client,user_create_url', [
    (app_flask_restplus.test_client(), '/user'),
    (app_ma_apispec.test_client(), '/user'),
    (app_flask_apispec.test_client(), '/user'),
])
def test_app_create_user(test_client, user_create_url):
    response = test_client.post(user_create_url, json={'name': 'foo'})
    assert response.status_code == 201
    assert_is_json(response)
    assert response.json['name'] == 'foo'
    assert response.json['id'] == 3


@pytest.mark.parametrize('test_client,user_update_url', [
    (app_flask_restplus.test_client(), '/user/2'),
    (app_ma_apispec.test_client(), '/user/2'),
    (app_flask_apispec.test_client(), '/user/2'),
])
def test_app_update_user(test_client, user_update_url):
    response = test_client.put(user_update_url, json={'name': 'foo'})
    assert response.status_code == 200
    assert_is_json(response)
    assert response.json['name'] == 'foo'
    assert response.json['id'] == 2
