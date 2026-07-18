class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def fill(self, selector: str, text: str):
        self.page.fill(selector, text)

    def click(self, selector: str, force: bool = False):
        self.page.click(selector, force=force)