from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Локаторы названий товаров
        self.PRODUCT_TITLES = "a[data-code], [data-code] a, [class*='Title'], .styles_productTitle__"
        # Гибкий селектор: ищет кнопку по классам или по тексту "В корзину" внутри карточки
        self.ADD_TO_CART_BUTTON = "button:has-text('В корзину'), button[class*='buyButton'], button[class*='toBasket']"
        # Иконка корзины в шапке сайта
        self.HEADER_CART_BUTTON = "header a[href*='basket'], .headerCart, [class*='basket']"

    def get_all_product_titles(self):
        self.page.wait_for_selector(self.PRODUCT_TITLES, timeout=15000)
        elements = self.page.locator(self.PRODUCT_TITLES).all()
        return [el.inner_text() for el in elements]

    def add_first_product_to_cart(self):
        """Нажать 'В корзину' на первом товаре и перейти в корзину"""
        # Сначала убеждаемся, что названия товаров загрузились
        self.page.wait_for_selector(self.PRODUCT_TITLES, timeout=15000)

        # Находим ПЕРВУЮ видимую карточку товара и кликаем в ней по кнопке корзины
        first_product = self.page.locator(self.PRODUCT_TITLES).first
        product_name = first_product.inner_text()

        # Находим саму кнопку корзины внутри каталога
        target_button = self.page.locator(self.ADD_TO_CART_BUTTON).first

        # Кликаем по ней напрямую через JavaScript (выполняет клик даже если элемент частично перекрыт)
        target_button.dispatch_event("click")

        # Обязательная пауза, чтобы корзина успела обновиться
        self.page.wait_for_timeout(1500)
        self.click(self.HEADER_CART_BUTTON, force=True)

        return product_name

