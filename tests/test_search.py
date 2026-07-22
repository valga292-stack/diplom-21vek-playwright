import pytest
import allure
import sqlite3
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage

def get_search_data_from_db():
    conn = sqlite3.connect("test_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            product_name TEXT NOT NULL
        )
    """)
    cursor.execute("DELETE FROM search_queries")
    full_queries = [
        ("утюг", "Утюг"), ("холодильник", "Холодильник"),
        ("стиральная машина", "Стир. машина"), ("микроволновка", "Микроволновка"),
        ("пылесос", "Пылесос"), ("телевизор", "Телевизор"),
        ("ноутбук", "Ноутбук"), ("смартфон", "Смартфон"),
        ("наушники", "Наушники"), ("планшет", "Планшет"),
        ("плита", "Плита"), ("духовой шкаф", "Духовой шкаф"),
        ("вытяжка", "Вытяжка"), ("посудомойка", "Посудомойка"),
        ("чайник", "Чайник"), ("блендер", "Блендер"),
        ("тостер", "Тостер"), ("кофемашина", "Кофемашина"),
        ("мясорубка", "Мясорубка"), ("миксер", "Миксер"),
        ("фен", "Фен"), ("утюжок", "Утюжок")
    ]
    cursor.executemany("INSERT INTO search_queries (query, product_name) VALUES (?, ?)", full_queries)
    conn.commit()
    cursor.execute("SELECT query, product_name FROM search_queries")
    data = cursor.fetchall()
    conn.close()
    return data

@allure.feature("Модуль: Поиск по сайту")
class TestSearch:

    @allure.story("Позитивный сценарий: Поиск товаров из базы данных")
    @pytest.mark.parametrize("search_query, expected_name", get_search_data_from_db())
    def test_search_shows_results_page(self, browser_page, search_query, expected_name):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Открыть главную страницу 21vek и ввести запрос: {search_query}"):
            home.open_home()
            home.search(search_query)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("2. Проверить, что на странице отображаются карточки товаров"):
            browser_page.wait_for_timeout(2000)
            cards_count = browser_page.locator(results.PRODUCT_TITLES).count()
            assert cards_count > 0, f"Товары по запросу '{search_query}' не найдены на странице!"

    @allure.story("Негативный сценарий: Поиск несуществующего товара")
    @pytest.mark.parametrize("invalid_query", ["abracadabra123", "@@@!!!", "несуществующийтоварэкзамен"])
    def test_negative_search_no_results(self, browser_page, invalid_query):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Ввести некорректный запрос: {invalid_query}"):
            home.open_home()
            home.search(invalid_query)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("2. Проверить, что на странице отсутствуют кнопки покупки товара"):
            browser_page.wait_for_timeout(2000)
            buy_buttons_count = browser_page.locator(results.ADD_TO_CART_BUTTON).count()
            assert buy_buttons_count == 0, f"Ошибка! Нашлось {buy_buttons_count} кнопок!"
