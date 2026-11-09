import random
import string
import allure
import requests
import urls

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_payload():
    random_part = generate_random_string(6)
    return {
        "email": f"test_user_{random_part}@yandex.ru",
        "password": f"pass_{random_part}",
        "name": f"Name_{random_part}"
    }

@allure.step("Получить список ингредиентов")
def get_ingredient_ids(count=2):
    response = requests.get(urls.INGREDIENTS_URL)
    ingredients = response.json()["data"]
    return [item["_id"] for item in ingredients[:count]]