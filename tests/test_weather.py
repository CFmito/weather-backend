import sys
from pathlib import Path

# Добавляем корневую директорию (двойные подчеркивания file)
sys.path.append(str(Path(file).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    assert True

def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200