# service-auth/tests/test_auth.py
import os
import time

os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_db"
os.environ["SECRET_KEY"] = "fake_secret_key_for_tests"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generer_username():
    """Générer un username unique"""
    return f"test_{int(time.time() * 1)}"


def test_register():
    """Test inscription"""
    
    username = generer_username()
    
    response = client.post("/Signup", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()


def test_login():
    """Test connexion"""
    
    username = generer_username()
    
    # S'inscrire d'abord
    client.post("/Signup", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "pass123"
    })
    
    # Se connecter
    response = client.post("/Login", json={
        "username": username,
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()