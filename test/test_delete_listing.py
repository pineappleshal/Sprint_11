import allure

from data import DELETE_SUCCESS


@allure.feature('Удаление объявления')
class TestDeleteListing:
    @allure.title('Владелец удаляет объявление, запись исчезает из его списка')
    def test_owner_deletes_listing(self, listings_api, created_listing):
        response = listings_api.delete(created_listing['id'])

        assert response.status_code == 200, response.text
        assert response.json() == DELETE_SUCCESS
        saved = listings_api.get_own()
        assert saved.status_code == 200, saved.text
        assert saved.json() == {'offers': [], 'totalPages': 0}
