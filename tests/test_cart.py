import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.cart_page import CartPage

@allure.feature("Модуль: Корзина")
class TestCart:

    @allure.story("Параметризованный E2E сценарий корзины")
    @pytest.mark.parametrize("product_to_cart", [
        "ноутбук", "смартфон", "пылесос",
    ])
    def test_add_and_remove_product_from_cart(self, browser_page, product_to_cart):
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

    @allure.story("Изменение количества товара и проверка пересчета стоимости")
    def test_cart_price_recalculation(self, browser_page):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)
        cart = CartPage(browser_page)

        with allure.step("1. Найти и добавить товар в корзину"):
            home.open_home()
            home.search("смартфон")
            results.add_first_product_to_cart()

        with allure.step("2. Перейти в корзину и зафиксировать базовую цену"):
            browser_page.goto("https://21vek.by")
            base_price = cart.get_product_price()

        with allure.step("3. Изменить состояние элемента — увеличить количество (нажать '+')"):
            cart.increase_product_count()
            new_price = cart.get_product_price()

        with allure.step("4. Проверить, что итоговая цена увеличилась"):
            assert new_price > base_price, f"Цена не пересчиталась! Было: {base_price}, стало: {new_price}"

        with allure.step("5. Очистить корзину"):
            cart.delete_product()


    @allure.story("Проверка отображения пустой корзины")
    def test_empty_cart_message(self, browser_page):
        cart = CartPage(browser_page)

        with allure.step("1. Перейти в заведомо пустую корзину"):
            browser_page.goto("https://21vek.by")

        with allure.step("2. Проверить наличие сообщения 'Корзина пуста'"):
            is_empty = browser_page.locator(cart.EMPTY_CART_MESSAGE).first.is_visible()
            assert is_empty, "Сообщение о пустой корзине не отображается!"
    @allure.story("Переход из корзины обратно к покупкам")
    def test_navigate_back_to_shopping(self, browser_page):
        cart = CartPage(browser_page)

        with allure.step("1. Перейти в пустую корзину"):
            browser_page.goto("https://21vek.by")

        with allure.step("2. Кликнуть по кнопке возврата к покупкам"):
            back_button = "a[class*='Empty_button'], button:has-text('Начать покупки'), a:has-text('Перейти к покупкам'), .cr-cart__empty a"
            browser_page.wait_for_selector(back_button, timeout=25000)
            browser_page.click(back_button, force=True)

        with allure.step("3. Проверить, что пользователь вернулся на главную страницу"):
            browser_page.wait_for_timeout(25000)
            assert browser_page.url == "https://21vek.by" or "21vek.by" in browser_page.url, "Не удалось вернуться на главную страницу!"
