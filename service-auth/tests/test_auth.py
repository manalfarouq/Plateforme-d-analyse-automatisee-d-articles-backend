# service-auth/tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    """Test inscription"""
    response = client.post("/Signup", json={
        "username": "test",
        "email": "test@mail.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()


def test_login():
    """Test connexion"""
    # S'inscrire d'abord
    client.post("/Signup", json={
        "username": "user1",
        "email": "user1@mail.com",
        "password": "pass123"
    })
    
    # Se connecter
    response = client.post("/Login", json={
        "username": "user1",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()