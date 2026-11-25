import allure
import pytest

from data import EDIT_CASES, FORBIDDEN_NAME, FOREIGN_EDIT_ERROR


@allure.feature('Редактирование объявления')
class TestEditListing:
    @allure.title('Владелец изменяет поле {field} и сохраняет остальные данные')
    @pytest.mark.parametrize('field,value', EDIT_CASES, ids=[case[0] for case in EDIT_CASES])
    def test_owner_updates_field(self, listings_api, created_listing, listing_data, field, value):
        expected = {**listing_data, field: value}
        response = listings_api.update(created_listing['id'], expected)

        assert response.status_code == 200, response.text
        body = response.json()
        assert body['id'] == created_listing['id']
        assert body['owner'] == created_listing['owner']
        assert body['createdAt'] == created_listing['createdAt']
        assert {key: body[key] for key in expected} == expected
        saved = listings_api.get_own()
        assert saved.status_code == 200, saved.text
        assert saved.json()['offers'] == [body]

    @allure.title('Другой пользователь не может изменить чужое объявление')
    def test_non_owner_cannot_update_listing(self, listings_api, other_listings_api,
                                            created_listing, listing_data, authorized_user, other_user):
        assert other_user.id != authorized_user.id
        changed = {**listing_data, 'name': FORBIDDEN_NAME}
        response = other_listings_api.update(created_listing['id'], changed)

        assert response.status_code == 401, response.text
        assert response.json() == FOREIGN_EDIT_ERROR
        saved = listings_api.get_own()
        assert saved.status_code == 200, saved.text
        assert saved.json()['offers'] == [created_listing], 'После отказа исходное объявление должно остаться неизменным'
