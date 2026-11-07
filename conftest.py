import pytest
import requests
import urls
from helpers import generate_user_payload

@pytest.fixture(scope="function")
def create_and_delete_user():
    """Фикстура для создания уникального пользователя и его удаления после теста."""
    payload = generate_user_payload()
    response = requests.post(urls.CREATE_USER_URL, json=payload)
    access_token = response.json().get("accessToken")
    
    yield payload, response, access_token

    # Очистка данных: удаляем пользователя, если токен был успешно получен
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(urls.USER_DATA_URL, headers=headers)