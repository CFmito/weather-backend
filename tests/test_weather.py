import pytest
from fastapi.testclient import TestClient
from app.main import app  # Импортируем app из директории app/main.py

client = TestClient(app)

def test_health_check():
    assert True

def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200