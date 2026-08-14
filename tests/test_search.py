import pytest
import allure
import sqlite3
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage

def get_search_data_from_db():
    conn = sqlite3.connect("test_data.db")
    cursor = conn.cursor()
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

        with allure.step(f"1. Открыть главную страницу и выполнить поиск: {search_query}"):
            home.open_home()
            home.search(search_query)

        with allure.step("2. Проверить результаты через Page Object метод"):
            results.verify_products_are_found(search_query)

    @allure.story("Негативный сценарий: Поиск несуществующего товара")
    @pytest.mark.parametrize("invalid_query", ["abracadabra123", "@@@!!!", "несуществующийтоварэкзамен"])
    def test_negative_search_no_results(self, browser_page, invalid_query):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Ввести некорректный запрос: {invalid_query}"):
            home.open_home()
            home.search(invalid_query)

        with allure.step("2. Верифицировать отсутствие выдачи через Page Object"):
            results.verify_no_products_found()