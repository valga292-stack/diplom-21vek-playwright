import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@allure.feature("Модуль: Поиск по сайту")
class TestSearch:

    @allure.story("Параметризованный поиск существующих товаров")
    @pytest.mark.parametrize(
        "search_query",
        [
            # Бытовая техника
            "холодильник",
            "стиральная машина",
            "микроволновка",
            "пылесос",
            "кофемашина",
            "чайник",
            "тостер",
            "утюг",
            # Электроника
            "телевизор",
            "планшет",
            "смартфон",
            "ноутбук",
            "наушники",
            # Бренды (латиница)
            "iPhone",
            "Samsung",
            "Xiaomi",
            "LG",
            "Asus",
            # Товары для дома и авто
            "кофе в зернах",
            "умный дом",
            "шуруповерт",
            "видеорегистратор",
        ],
    )
    def test_search_shows_results_page(self, browser_page, search_query):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)

        with allure.step(
            f"1. Открыть главную страницу 21vek и ввести запрос: {search_query}"
        ):
            home.open_home()
            home.search(search_query)

        with allure.step("2. Проверить, что на странице отображаются карточки товаров"):
            is_visible = browser_page.locator(
                results.PRODUCT_TITLES
            ).first.is_visible()
            assert (
                is_visible
            ), f"Товары по запросу '{search_query}' не найдены на странице!"

    @allure.story("Негативный сценарий: Поиск несуществующего товара")
    @pytest.mark.parametrize("invalid_query", ["abracadabra123", "@@@!!!", "несуществующийтоварэкзамен"])
    def test_negative_search_no_results(self, browser_page, invalid_query):
        home = HomePage(browser_page)
        results = SearchResultsPage(browser_page)

        with allure.step(f"1. Ввести некорректный запрос: {invalid_query}"):
            home.open_home()
            home.search(invalid_query)

        with allure.step("2. Проверить, что на странице отсутствуют кнопки покупки товара"):
            browser_page.wait_for_load_state("domcontentloaded")
            # Считаем количество кнопок добавления в корзину на странице
            buy_buttons_count = browser_page.locator(results.ADD_TO_CART_BUTTON).count()

            # Строгая проверка: если поиск пустой, кнопок "В корзину" быть не должно!
            assert buy_buttons_count == 0, f"Ошибка! Для мусорного запроса на странице нашлось {buy_buttons_count} кнопок покупки!"
