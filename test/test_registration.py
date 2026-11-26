import allure

from api.listings_api import ListingsApi
from data import DUPLICATE_EMAIL_ERROR


@allure.feature('Регистрация пользователя')
class TestRegistration:
    @allure.title('Регистрация с новым email создаёт пользователя и выдаёт рабочий токен')
    def test_register_with_unique_email(self, auth_api, user_data, http_client):
        response = auth_api.register(user_data)
        body = response.json()
        token = body['access_token']['access_token']
        profile = ListingsApi(http_client, token).get_own()
        profile_body = profile.json()

        assert response.status_code == 201, response.text
        assert body['user']['email'] == user_data.email
        assert isinstance(body['user']['id'], int) and body['user']['id'] > 0
        assert isinstance(token, str) and token
        assert profile.status_code == 200, profile.text
        assert profile_body == {'offers': [], 'totalPages': 0}

    @allure.title('Повторная регистрация занятого email возвращает ошибку')
    def test_register_with_existing_email(self, auth_api, registered_user):
        response = auth_api.register(registered_user.credentials)
        body = response.json()

        assert response.status_code == 400, response.text
        assert body == DUPLICATE_EMAIL_ERROR
