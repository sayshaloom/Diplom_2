import pytest
import requests
import allure
import urls
from helpers import generate_user_payload

@allure.feature("Тестирование API Stellar Burgers")
@allure.story("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, create_and_delete_user):
        _, response, _ = create_and_delete_user

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_existing_user_forbidden(self, create_and_delete_user):
        existing_user_payload, _, _ = create_and_delete_user
        
        # Пытаемся создать пользователя с теми же данными повторно
        response = requests.post(urls.CREATE_USER_URL, json=existing_user_payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "User already exists"

    @allure.title("Ошибка при создании пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_forbidden(self, missing_field):
        payload = generate_user_payload()
        payload.pop(missing_field)  # Удаляем одно из полей
        
        response = requests.post(urls.CREATE_USER_URL, json=payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields"