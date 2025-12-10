# service-auth/app/auth/token_auth.py

from fastapi import Header, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from ..core.config import settings


def verify_token(token: str = Header(...)):
    """
    Vérifie le token JWT pour l'authentification.
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


def get_user_id_from_token(token: str):
    """
    Extrait l'user_id depuis le token JWT.
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


def create_jwt_token(user_id: int, username: str, email: str = None):
    """
    Crée un token JWT pour un utilisateur.
    Réutilisable pour login et register.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire
    }
    if email:
        payload["email"] = email
    
    return jwt.encode(payload, settings.SK, algorithm=settings.ALG)