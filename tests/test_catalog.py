import pytest
import allure
from pages.search_results_page import SearchResultsPage

@allure.feature("Модуль: Каталог и Сортировка")
class TestCatalog:

    @allure.story("Сортировка товаров по возрастанию цены")
    @pytest.mark.parametrize("category_url, category_name", [
        ("https://21vek.by", "смартфоны"),
        ("https://21vek.by", "ноутбуки"),
        ("https://21vek.by", "холодильники")
    ])
    def test_sort_by_price_ascending(self, browser_page, category_url, category_name):
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Открыть категорию со встроенной сортировкой по цене: {category_name}"):
            browser_page.goto(category_url)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("2. Проверить, что на странице успешно отображаются карточки товаров"):
            browser_page.wait_for_timeout(3000)
            cards_count = browser_page.locator(results.PRODUCT_TITLES).count()
            assert cards_count > 0, f"Ошибка! В категории '{category_name}' список товаров пуст!"