import allure

from api.listings_api import ListingsApi
from data import DUPLICATE_EMAIL_ERROR


@allure.feature('Регистрация пользователя')
class TestRegistration:
    @allure.title('Регистрация с новым email создаёт пользователя и выдаёт рабочий токен')
    def test_register_with_unique_email(self, auth_api, user_data, http_client):
        response = auth_api.register(user_data)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body['user']['email'] == user_data.email
        assert isinstance(body['user']['id'], int) and body['user']['id'] > 0
        token = body['access_token']['access_token']
        assert isinstance(token, str) and token
        profile = ListingsApi(http_client, token).get_own()
        assert profile.status_code == 200, profile.text
        assert profile.json() == {'offers': [], 'totalPages': 0}

    @allure.title('Повторная регистрация занятого email возвращает ошибку')
    def test_register_with_existing_email(self, auth_api, registered_user):
        response = auth_api.register(registered_user.credentials)

        assert response.status_code == 400, response.text
        assert response.json() == DUPLICATE_EMAIL_ERROR
