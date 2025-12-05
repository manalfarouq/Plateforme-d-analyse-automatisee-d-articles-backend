from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
from ..core.config import settings

def verify_token(token: str = Header(...)):
    """
    Vérifie le token JWT pour l'authentification.
    Args:
        token (str): Le token JWT à vérifier.
    Raises:
        HTTPException: Si le token est invalide ou expiré.
    Returns:
        dict: Les données du token décodées.
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")