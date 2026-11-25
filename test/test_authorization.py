import allure

from api.listings_api import ListingsApi


@allure.feature('Авторизация пользователя')
class TestAuthorization:
    @allure.title('Вход зарегистрированного пользователя возвращает его данные и рабочий токен')
    def test_login_registered_user(self, auth_api, registered_user, http_client):
        response = auth_api.login(registered_user.credentials)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body['user']['id'] == registered_user.id
        assert body['user']['email'] == registered_user.email
        token = body['token']['access_token']
        assert isinstance(token, str) and token
        profile = ListingsApi(http_client, token).get_own()
        assert profile.status_code == 200, profile.text
        assert profile.json() == {'offers': [], 'totalPages': 0}
