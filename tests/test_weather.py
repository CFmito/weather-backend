import pytest
from fastapi.testclient import TestClient
from app.main import app  # Если главный файл FastAPI находится в app/main.py

client = TestClient(app)

def test_health_check():
    """Базовый тест для проверки, что тест-фреймворк работает"""
    assert True

def test_read_main():
    """Тест проверки доступности корневого эндпоинта или документации"""
    response = client.get("/docs")
    assert response.status_code == 200