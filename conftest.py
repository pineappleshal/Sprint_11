import allure
import pytest

from api.auth_api import AuthApi
from api.http_client import HttpClient
from api.listings_api import ListingsApi
from data import DELETE_SUCCESS, LISTING_DATA
from helpers.generators import generate_credentials
from helpers.models import User


@pytest.fixture
def http_client():
    client = HttpClient()
    yield client
    client.close()


@pytest.fixture
def auth_api(http_client):
    return AuthApi(http_client)


@pytest.fixture
def user_data():
    return generate_credentials()


@pytest.fixture
def registered_user(auth_api, user_data):
    with allure.step('Зарегистрировать отдельного пользователя для предусловий'):
        response = auth_api.register(user_data)
        assert response.status_code == 201, response.text
        body = response.json()
        return User(body['user']['id'], body['user']['email'], user_data, body['access_token']['access_token'])


@pytest.fixture
def authorized_user(auth_api, registered_user):
    with allure.step('Авторизовать владельца тестового объявления'):
        response = auth_api.login(registered_user.credentials)
        assert response.status_code == 201, response.text
        body = response.json()
        assert body['user']['id'] == registered_user.id
        return User(registered_user.id, registered_user.email, registered_user.credentials, body['token']['access_token'])


@pytest.fixture
def other_user(auth_api):
    with allure.step('Создать и авторизовать второго пользователя'):
        credentials = generate_credentials()
        registration = auth_api.register(credentials)
        assert registration.status_code == 201, registration.text
        login = auth_api.login(credentials)
        assert login.status_code == 201, login.text
        body = login.json()
        return User(body['user']['id'], body['user']['email'], credentials, body['token']['access_token'])


@pytest.fixture
def listings_api(http_client, authorized_user):
    api = ListingsApi(http_client, authorized_user.token)
    yield api
    with allure.step('Удалить оставшиеся объявления созданного для теста пользователя'):
        response = api.get_own()
        assert response.status_code == 200, response.text
        for offer in response.json()['offers']:
            assert offer['owner'] == authorized_user.id
            deleted = api.delete(offer['id'])
            assert deleted.status_code == 200, deleted.text
            assert deleted.json() == DELETE_SUCCESS


@pytest.fixture
def other_listings_api(http_client, other_user):
    return ListingsApi(http_client, other_user.token)


@pytest.fixture
def listing_data():
    return LISTING_DATA.copy()


@pytest.fixture
def created_listing(listings_api, listing_data):
    with allure.step('Создать объявление для предусловий'):
        response = listings_api.create(listing_data)
        assert response.status_code == 201, response.text
        return response.json()
