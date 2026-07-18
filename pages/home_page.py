from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    URL = "http://21vek.by"
    SEARCH_INPUT = "input#catalogSearch"
    SEARCH_BUTTON = "button.Search_searchBtn__Tk7Gw"
    COOKIE_ACCEPT_BUTTON = "button[class*='accept'], #modal-cookie button"

    def open_home(self):
        self.open(self.URL)
        try:
            self.page.wait_for_selector(self.COOKIE_ACCEPT_BUTTON, timeout=2000)
            self.click(self.COOKIE_ACCEPT_BUTTON)
        except Exception:
            pass

    def search(self, text: str):
        self.fill(self.SEARCH_INPUT, text)
        self.click(self.SEARCH_BUTTON, force=True)
        # Ждем, пока прекратятся сетевые запросы, чтобы страница выдачи гарантированно загрузилась
        self.page.wait_for_load_state("networkidle")
