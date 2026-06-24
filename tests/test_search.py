import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@allure.feature("Модуль: Поиск по сайту")
@allure.story("Параметризованный поиск товаров")
@pytest.mark.parametrize("search_query", [
    "телефон",
    "smartphone",
    "ноутбук"
])
def test_search_shows_results_page(browser_page, search_query):
    home = HomePage(browser_page)
    results = SearchResultsPage(browser_page)

    with allure.step(f"Открыть главную страницу 21vek и ввести запрос: '{search_query}'"):
        home.open_home()
        home.search(search_query)

    with allure.step("Проверить результаты поисковой выдачи"):
        titles = results.get_all_product_titles()
        assert len(titles) > 0, f"По запросу '{search_query}' маркетплейс не вернул ни одного товара!"