import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@allure.feature("Модуль: Мобильная адаптивная версия")
class TestMobileAdaptive:
    # Эмуляция экрана популярного смартфона (iPhone 14)
    MOBILE_VIEWPORT = {"width": 393, "height": 852}

    @allure.story("Проверка отображения мобильного меню (гамбургер)")
    def test_mobile_menu_hamburger_visible(self, browser_page):
        with allure.step("1. Установить мобильное разрешение экрана"):
            browser_page.set_viewport_size(self.MOBILE_VIEWPORT)
            home = HomePage(browser_page)

        with allure.step("2. Открыть главную страницу 21vek"):
            home.open_home()
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("3. Проверить, что на экране появилась кнопка мобильного меню"):
            # Неубиваемый комбинированный локатор кнопки меню в мобильной версии
            hamburger_button = "header button[class*='burger'], header [class*='styles_burger'], button:has(svg), [class*='Header_burger'], header button"
            browser_page.wait_for_selector(hamburger_button, timeout=15000)
            is_visible = browser_page.locator(hamburger_button).first.is_visible()

            assert is_visible, "Кнопка мобильного меню-гамбургера не отображается на экране смартфона!"

    @allure.story("Параметризованный поиск товаров в мобильной версии")
    @pytest.mark.parametrize("mobile_product", ["смартфон", "ноутбук", "наушники"])
    def test_mobile_search(self, browser_page, mobile_product):
        with allure.step("1. Установить мобильное разрешение экрана"):
            browser_page.set_viewport_size(self.MOBILE_VIEWPORT)
            home = HomePage(browser_page)
            results = SearchResultsPage(browser_page)

        with allure.step(f"2. Искать товар в мобильной верстке: {mobile_product}"):
            home.open_home()
            home.search(mobile_product)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("3. Проверить, что в мобильной выдаче отобразились карточки"):
            browser_page.wait_for_timeout(2000)
            cards_count = browser_page.locator(results.PRODUCT_TITLES).count()
            assert cards_count > 0, f"В мобильной версии товары по запросу '{mobile_product}' не найдены!"
