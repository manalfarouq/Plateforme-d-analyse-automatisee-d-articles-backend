from fastapi import APIRouter, HTTPException
from ..schemas.SignupRequest_schema import SignupRequest
from ..database.db_connection import get_db_connection  
import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from ..core.config import settings


router = APIRouter()


@router.post("/Signup")
def register(signup_request: SignupRequest):
    """
    Endpoint pour l'inscription des nouveaux utilisateurs.
    Vérifie que le username n'existe pas déjà et crée un nouveau compte.
    Route simple de signup :
    - Vérifie si le username existe déjà
    - Hash le mot de passe avec bcrypt
    - Insère le nouvel utilisateur dans la base
    - Retourne un message de succès
    """
    
    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        #!  Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT username FROM users WHERE username = %s", (signup_request.username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà.")
        
        #! Hasher le mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(signup_request.password.encode('utf-8'), bcrypt.gensalt())
        
        #! Insérer le nouvel utilisateur avec email
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",  
            (signup_request.username, hashed_password.decode('utf-8'), signup_request.email)
        )
        
        #! Sauvegarder les changements dans la base
        conn.commit()
        
        #! Créer un JWT token
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        token = jwt.encode(
            {"sub": signup_request.username, "email": signup_request.email, "exp": expire},
            settings.SK,
            algorithm=settings.ALG
        )
        
        #! Retourner un message de succès avec token
        return {
            "message": "Utilisateur créé avec succès",
            "username": signup_request.username,
            "email": signup_request.email,
            "token": token
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()