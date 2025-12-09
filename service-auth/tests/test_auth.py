# service-auth/tests/test_auth.py
import os
import random
import string

os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_db"
os.environ["SECRET_KEY"] = "fake_secret_key_for_tests"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generer_username_unique():
    """Générer un username aléatoire"""
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def test_register():
    """Test inscription"""
    
    username = generer_username_unique()
    
    response = client.post("/Signup", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()


def test_login():
    """Test connexion"""
    
    username = generer_username_unique()
    
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