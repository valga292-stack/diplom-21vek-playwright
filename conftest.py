import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # headless=True — это секрет, который обойдёт блокировку Windows Smart App Control!
        # Когда браузер работает в фоне, система не видит в нём угрозы и не блокирует библиотеки.
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def browser_page(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU"
    )
    page = context.new_page()
    yield page
    context.close()




