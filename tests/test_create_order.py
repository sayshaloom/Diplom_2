import requests
import allure
import urls

from helpers import get_ingredient_ids

@allure.feature("Тестирование API Stellar Burgers")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth_success(self, create_and_delete_user):
        _, _, access_token = create_and_delete_user
        
        order_payload = {"ingredients": get_ingredient_ids()}
        
        headers = {"Authorization": access_token}
        response = requests.post(urls.CREATE_ORDER_URL, json=order_payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_without_auth_success(self):

        order_payload = {"ingredients": get_ingredient_ids()}

        # Запрос уходит без заголовка Authorization
        response = requests.post(urls.CREATE_ORDER_URL, json=order_payload)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка создания заказа без ингредиентов")
    def test_create_order_without_ingredients_bad_request(self):
        order_payload = {"ingredients": []}
        response = requests.post(urls.CREATE_ORDER_URL, json=order_payload)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Ошибка создания заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash_server_error(self):
        order_payload = {
            "ingredients": ["invalid_hash_1", "invalid_hash_2"]
        }
        response = requests.post(urls.CREATE_ORDER_URL, json=order_payload)
        
        assert response.status_code == 500