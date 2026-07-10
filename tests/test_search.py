import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@allure.feature("Модуль: Поиск по сайту")
@allure.story("Параметризованный поиск товаров")
@pytest.mark.parametrize("search_query", [
    # Бытовая техника
    "холодильник", "стиральная машина", "микроволновка", "пылесос", "кофемашина", "чайник", "тостер", "утюг"
    # Электроникатер
    "телевизор", "планшет", "смартфон", "ноутбук", "наушники"
    # Бренды (латиница)
    "iPhone", "Samsung", "Xiaomi", "LG", "Asus",
    # Товары для дома и авто
    "кофе в зернах", "умный дом", "шуруповерт", "видеорегистратор",
    # Негативный сценарий (поиск несуществующего товара)
    "abracadabra123"
])
def test_search_shows_results_page(browser_page, search_query):
    home = HomePage(browser_page)
    results = SearchResultsPage(browser_page)

    with allure.step(f"Открыть главную страницу 21vek и ввести запрос: '{search_query}'"):
        home.open_home()
        home.search(search_query)

    with allure.step("Проверить результаты поисковой выдачи"):
        if search_query == "abracadabra123":
            # Для несуществующего товара проверяем, что страница просто загрузилась
            assert browser_page.locator("body").is_visible()
        else:
            titles = results.get_all_product_titles()
            assert len(titles) > 0, f"По запросу '{search_query}' маркетплейс не вернул ни одного товара!"


