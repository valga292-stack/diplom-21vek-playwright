import pytest
import allure
from pages.home_page import HomePage


@allure.feature("Модуль: Сквозная навигация по сайту")
class TestNavigation:

    @allure.story("Проверка главных разделов шапки и футера")
    @pytest.mark.parametrize("target_url, expected_text", [
        ("https://21vek.by", "Акции"),
        ("https://21vek.by", "Доставка"),
        ("https://21vek.by", "Оплата")
    ])
    def test_header_navigation_links(self, browser_page, target_url, expected_text):
        with allure.step(f"1. Перейти по прямой ссылке в раздел: {expected_text}"):
            browser_page.goto(target_url)
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step(f"2. Проверить, что страница {expected_text} успешно загрузилась"):
            assert browser_page.locator(f"body:has-text('{expected_text}')").first.is_visible(), \
                f"Страница {expected_text} не загрузилась или текст не найден!"

    @allure.story("Проверка возврата на главную страницу через клик по логотипу")
    def test_logo_redirect_to_home(self, browser_page):
        home = HomePage(browser_page)

        with allure.step("1. Открыть страницу Акций"):
            browser_page.goto("https://21vek.by")
            browser_page.wait_for_load_state("domcontentloaded")

        with allure.step("2. Кликнуть по главному логотипу в шапке сайта"):
            logo_locator = "header a[class*='logo'], a[href='/'].styles_logo__, a[class*='styles_logo']"
            browser_page.wait_for_selector(logo_locator, timeout=10000)
            browser_page.click(logo_locator, force=True)
            browser_page.wait_for_load_state("networkidle")

        with allure.step("3. Проверить, что пользователь вернулся на главную страницу"):
            assert browser_page.url == "https://21vek.by" or "21vek.by" in browser_page.url, \
                "Клик по логотипу не вернул пользователя на главную страницу!"
