from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().init(page)

    PRODUCT_TITLE = "a[class*='Item_title'], [class*='title'], [class*='ItemTitle'], a[href*='product']"

    # Сверхширокий локатор кнопки удаления: ищет любую кнопку или ссылку со словом 'Удалить' или 'delete' в коде
    DELETE_BUTTON = "button:has-text('Удалить'), [aria-label*='Удалить'], [aria-label*='delete'], button[class*='delete'], button[class*='remove'], [class*='deleteButton']"

    EMPTY_CART_MESSAGE = "[class*='Empty'], :has-text('Корзина пуста'), :has-text('пуста')"

    def get_product_title_in_cart(self):
        """Получить название товара, лежащего в корзине"""
        self.page.wait_for_selector(self.PRODUCT_TITLE, timeout=10000)
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text()

    def delete_product(self):
        """Удалить товар из корзины"""
        # Сначала пробуем подождать универсальный локатор
        try:
            self.page.wait_for_selector(self.DELETE_BUTTON, timeout=5000, state="attached")
            self.click(self.DELETE_BUTTON, force=True)
        except Exception:
            # План Б: если классы скрыты, кликаем по первому попавшемуся тегу 'button' внутри блока товара,
            # содержащему иконку удаления (обычно это и есть кнопка крестика)
            self.page.locator("button[class*='Item_']").first.click(force=True)

        # Даем сайту 2 секунды на отработку анимации удаления и пересчет корзины
        self.page.wait_for_timeout(2000)

    def is_cart_empty(self):
        """Проверить, появилось ли сообщение о пустой корзине"""
        try:
            self.page.wait_for_selector(self.EMPTY_CART_MESSAGE, timeout=5000)
            return self.page.locator(self.EMPTY_CART_MESSAGE).first.is_visible()
        except Exception:
            return False
