import requests


def test_api_catalog_status():
    """Тест API: Проверка доступности главного сервера 21vek.by"""
    # Отправляем быстрый GET-запрос к главной странице через стандартную библиотеку requests
    response = requests.get("https://21vek.by", timeout=10)

    # Жестко проверяем, что сервер возвращает статус 200 ОК (сайт живой)
    assert response.status_code == 200, f"Сервер недоступен, статус: {response.status_code}"
