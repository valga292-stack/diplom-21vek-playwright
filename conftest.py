import pytest
from playwright.sync_api import sync_playwright
import sqlite3
from datetime import datetime

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
    page.set_default_timeout(60000)
    yield page
    context.close()


import sqlite3
import pytest
from datetime import datetime


@pytest.fixture(scope="session", autouse=True)
def log_to_database():
    """Фикстура БД: Логирование времени запуска тестовой сессии в базу SQLite"""
    # Создаем подключение к базе данных в памяти (она уничтожится после тестов)
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создаем простую таблицу для логов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            timestamp TEXT
        )
    """)

    # Записываем событие старта
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO test_logs (event_name, timestamp) VALUES (?, ?)",
        ("Test Session Started", current_time)
    )
    conn.commit()

    yield

    # Закрываем соединение после окончания всех тестов
    conn.close()



