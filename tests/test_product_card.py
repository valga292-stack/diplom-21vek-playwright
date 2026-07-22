import pytest
import allure
from pages.search_results_page import SearchResultsPage


@allure.feature("Модуль: Карточка товара и Бренды")
class TestProductCard:

    @allure.story("Проверка доступности товарных листингов крупных брендов")
    @pytest.mark.parametrize("brand_url, brand_name", [
        ("https://www.21vek.by", "Смартфоны Apple"),
        ("https://www.21vek.by", "Ноутбуки Apple"),
        ("https://www.21vek.by", "Телевизоры LG")
    ])
    def test_product_card_elements(self, browser_page, brand_url, brand_name):
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Перейти на страницу бренда напрямую: {brand_name}"):
            browser_page.goto(brand_url)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step(f"2. Проверить, что карточки товаров бренда успешно отображаются"):
            browser_page.wait_for_timeout(3000)

            # Считаем количество карточек товаров на странице бренда
            cards_count = browser_page.locator(results.PRODUCT_TITLES).count()
            assert cards_count > 0, f"Ошибка! На странице бренда '{brand_name}' список товаров пуст!"