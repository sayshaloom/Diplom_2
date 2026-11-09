import requests
import allure
import urls

@allure.feature("Тестирование API Stellar Burgers")
@allure.story("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, create_and_delete_user):
        user_payload, _, _ = create_and_delete_user
        
        login_payload = {
            "email": user_payload["email"],
            "password": user_payload["password"]
        }
        response = requests.post(urls.LOGIN_USER_URL, json=login_payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при входе с неверным логином или паролем")
    def test_login_with_incorrect_credentials_unauthorized(self):
        incorrect_payload = {
            "email": "wrong_email_format_12345@yandex.ru",
            "password": "wrong_password"
        }
        response = requests.post(urls.LOGIN_USER_URL, json=incorrect_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"
