from ..schemas.LoginRequest_schema import LoginRequest
from fastapi import APIRouter, HTTPException
from ..database.db_connection import get_db_connection
from jose import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from ..core.config import settings


router = APIRouter()

@router.post("/Login")
def login(login_request: LoginRequest):
    """
    Endpoint pour connecter un utilisateur.
    Args:
        login_request (LoginRequest): Contient le nom d'utilisateur et le mot de passe.
    Returns:
        dict: Token d'accès JWT si les informations d'identification sont valides.
    """
    conn = None  
    cursor = None  
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Récupérer l'utilisateur par nom d'utilisateur
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (login_request.username,))
        user = cursor.fetchone()
        
        if user is None:
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe invalide")
        
        user_id, username, password_hash = user
        
        # Vérifier le mot de passe
        if not bcrypt.checkpw(login_request.password.encode('utf-8'), password_hash.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe invalide")

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id), 
            "username": username,
            "exp": expire  
        }
        token = jwt.encode(payload, settings.SK, algorithm=settings.ALG)
        
        return {
            "token": token,
            "user_id": user_id,
            "username": username
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        # Log l'erreur mais ne l'expose pas à l'utilisateur
        print(f"Erreur login: {str(e)}")  
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la connexion"  
        )
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()