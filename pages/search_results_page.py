from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().init(page)

    # Локаторы названий товаров
    PRODUCT_TITLES = "span.resultname, [class*='title'], [class*='name'], .styles_productTitle"

    # Гибкий селектор: ищет кнопку по классам ИЛИ по тексту "В корзину" внутри карточки
    ADD_TO_CART_BUTTON = "button:has-text('В корзину'), button[class*='buyButton'], button[class*='toBasket']"

    # Иконка корзины в шапке сайта
    HEADER_CART_BUTTON = "header a[href*='basket'], .headerCart, [class*='basket']"

    def get_all_product_titles(self):
        self.page.wait_for_selector(self.PRODUCT_TITLES, timeout=5000)
        elements = self.page.locator(self.PRODUCT_TITLES).all()
        return [el.inner_text() for el in elements]

    def add_first_product_to_cart(self):
        """Нажать 'В корзину' на первом товаре и перейти в корзину"""
        self.page.wait_for_selector(self.PRODUCT_TITLES, timeout=5000)
        product_name = self.page.locator(self.PRODUCT_TITLES).first.inner_text()

        # Ждем кнопку добавления и кликаем
        self.page.wait_for_selector(self.ADD_TO_CART_BUTTON, timeout=5000)
        self.click(self.ADD_TO_CART_BUTTON, force=True)

        # Небольшая пауза, чтобы сайт успел зафиксировать товар в сессии
        self.page.wait_for_timeout(1000)

        # Переходим в корзину
        self.page.wait_for_selector(self.HEADER_CART_BUTTON, timeout=5000)
        self.click(self.HEADER_CART_BUTTON, force=True)

        # Ждем загрузки страницы корзины
        self.page.wait_for_load_state("networkidle")

        return product_name
