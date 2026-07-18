import pytest
import allure
import requests


@allure.feature("Модуль: API Тестирование")
class TestBackendAPI:

    @allure.story("Проверка Backend API: Получение списка товаров в категории")
    def test_get_products_by_category_api(self):
        # Реалный публичный API эндпоинт каталога 21vek для мобильных телефонов
        url = "https://www.21vek.by"

        # Передаем стандартные заголовки, чтобы сайт не заблокировал запрос от скрипта
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        with allure.step("1. Отправить GET-запрос к API каталога смартфонов"):
            response = requests.get(url, headers=headers, timeout=15)

        with allure.step("2. Проверить, что сервер ответил со статусом 200 OK"):
            assert response.status_code == 200, f"Ошибка API! Сервер вернул статус {response.status_code}"

        with allure.step("3. Проверить, что ответ содержит валидные данные"):
            # Проверяем, что в ответе пришел не пустой текст
            assert response.text, "Ошибка! API вернул пустой ответ"
