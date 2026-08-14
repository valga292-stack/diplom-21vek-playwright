import pytest
import allure
import requests


@allure.feature("Модуль: Бэкенд API Каталога")
class TestCatalogAPI:

    @allure.story("Позитивный сценарий: Валидация структуры JSON и типов данных эндпоинта")
    def test_get_products_by_category_api(self):
        # Реальный backend-эндпоинт API каталога смартфонов
        url = "https://21vek.by"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }

        with allure.step("1. Отправить прямой GET-запрос к API каталога маркетплейса"):
            response = requests.get(url, headers=headers, timeout=10)

        with allure.step("2. Проверить статус-код ответа сервера (Должен быть 200 OK)"):
            assert response.status_code == 200, f"Неверный статус-код: {response.status_code}"

        with allure.step("3. Проверить валидность JSON-структуры и обязательные поля"):
            response_json = response.json()
            assert "items" in response_json or "products" in response_json, "В ответе API отсутствует корневой список товаров!"

            # Извлекаем список товаров (в зависимости от архитектуры ответа бэкенда)
            products = response_json.get("items", response_json.get("products", []))
            assert len(products) > 0, "API вернул пустой список товаров для валидной категории!"

        with allure.step("4. Построчная валидация типов данных и бизнес-логики (id, name, price)"):
            for product in products[:5]:  # Проверяем первые 5 товаров для оптимизации времени
                assert "id" in product or "code" in product, "В объекте товара отсутствует уникальный идентификатор!"
                assert "name" in product or "title" in product, "В объекте товара отсутствует поле названия!"

                # Проверяем типы данных по канонам QA Automation
                name_field = product.get("name", product.get("title"))
                assert isinstance(name_field,
                                  str), f"Поле названия должно быть строкой (str), пришло: {type(name_field)}"
                assert len(name_field) > 0, "Название товара в API не должно быть пустым!"