# service-auth/tests/test_auth.py
import os
import random
import string

os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_db"
os.environ["SECRET_KEY"] = "fake_secret_key_for_tests"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    """Test inscription"""
    
    response = client.post("/Signup", json={
        "username": "zoro",
        "email": "zoro@mail.com",
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()


def test_login():
    """Test connexion"""
    
    # S'inscrire d'abord
    client.post("/Signup", json={
        "username": "zoro1",
        "email": "zoro1@mail.com",
        "password": "pass123"
    })
    
    # Se connecter
    response = client.post("/Login", json={
        "username": "zoro1",
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()