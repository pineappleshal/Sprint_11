import allure
import pytest

from data import CREATE_CATEGORIES


@allure.feature('Создание объявления')
class TestCreateListing:
    @allure.title('Создание объявления в категории «{category}» сохраняет все поля')
    @pytest.mark.parametrize('category', CREATE_CATEGORIES, ids=['auto', 'books', 'technology'])
    def test_create_listing_in_category(self, listings_api, authorized_user, listing_data, category):
        expected = {**listing_data, 'category': category}
        response = listings_api.create(expected)

        assert response.status_code == 201, response.text
        body = response.json()
        assert isinstance(body['id'], int) and body['id'] > 0
        assert body['owner'] == authorized_user.id
        assert {key: body[key] for key in expected} == expected
        saved = listings_api.get_own()
        assert saved.status_code == 200, saved.text
        assert saved.json()['offers'] == [body]
