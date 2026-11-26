import allure

from data import DELETE_SUCCESS


@allure.feature('Удаление объявления')
class TestDeleteListing:
    @allure.title('Владелец удаляет объявление, запись исчезает из его списка')
    def test_owner_deletes_listing(self, listings_api, created_listing):
        response = listings_api.delete(created_listing['id'])
        body = response.json()
        saved = listings_api.get_own()
        saved_body = saved.json()

        assert response.status_code == 200, response.text
        assert body == DELETE_SUCCESS
        assert saved.status_code == 200, saved.text
        assert saved_body == {'offers': [], 'totalPages': 0}
