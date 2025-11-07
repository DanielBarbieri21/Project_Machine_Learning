"""
Testes para a API.
"""
import pytest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_health_check():
    """Testa o health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    """Testa a rota raiz."""
    response = client.get("/")
    assert response.status_code == 200


def test_list_models():
    """Testa listagem de modelos."""
    response = client.get("/models")
    assert response.status_code == 200
    assert "models" in response.json()

