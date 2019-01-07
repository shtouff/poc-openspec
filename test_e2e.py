import pytest

from app_flask_restplus import app as app_flask_restplus
from app_ma_apispec import app as app_ma_apispec
from app_flask_apispec import app as app_flask_apispec


def assert_is_json(response):
    assert hasattr(response, 'json')


def assert_1st_user_is_remi(test_client, url):
    response = test_client.get(url)
    assert_is_json(response)
    assert response.json[0].get('name') == 'remi'


def assert_swagger_is_ok(test_client, url):
    response = test_client.get(url)
    assert_is_json(response)
    assert response.json.get('swagger') == '2.0'


@pytest.mark.parametrize('test_client,user_list_url,swagger_url', [
    (app_flask_restplus.test_client(), '/user', '/swagger.json'),
    (app_ma_apispec.test_client(), '/user', '/swagger.json'),
    (app_flask_apispec.test_client(), '/user', '/swagger/'),
])
def test_app(test_client, user_list_url, swagger_url):
    assert_1st_user_is_remi(test_client, user_list_url)
    assert_swagger_is_ok(test_client, swagger_url)


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
