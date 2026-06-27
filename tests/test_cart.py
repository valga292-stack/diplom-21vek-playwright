import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.cart_page import CartPage

@allure.feature("Модуль: Корзина")
@allure.story("Параметризованный E2E сценарий корзины")
@pytest.mark.parametrize("product_to_cart", [
    "ноутбук", "смартфон", "пылесос",
])
def test_add_and_remove_product_from_cart(browser_page, product_to_cart):
    home = HomePage(browser_page)
    results = SearchResultsPage(browser_page)
    cart = CartPage(browser_page)

    with allure.step(f"1. Открыть главную страницу 21vek и найти: {product_to_cart}"):
        home.open_home()
        home.search(product_to_cart)

    with allure.step("2. Добавить первый товар в корзину и перейти в неё"):
        expected_name = results.add_first_product_to_cart()

    with allure.step("3. Проверить конкретику: в корзину попал именно тот товар"):
        actual_name = cart.get_product_title_in_cart()
        assert expected_name in actual_name, f"Ожидали товар '{expected_name}', а в корзине лежит '{actual_name}'"

    with allure.step("4. Удалить товар из корзины и проверить, что она пуста"):
        cart.delete_product()
        assert cart.is_cart_empty(), "Корзина не стала пустой после удаления товара!"

