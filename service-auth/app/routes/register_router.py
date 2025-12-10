# service-auth/app/routes/register_router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.SignupRequest_schema import SignupRequest
from ..database.db_connection import get_db
from ..models.user import User
from ..auth.token_auth import create_jwt_token
import bcrypt

router = APIRouter()


@router.post("/Signup")
def register(signup_request: SignupRequest, db: Session = Depends(get_db)):
    """
    Endpoint pour l'inscription des nouveaux utilisateurs avec SQLAlchemy.
    """
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.username == signup_request.username).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà")
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(
            signup_request.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Créer un nouvel utilisateur
        new_user = User(
            username=signup_request.username,
            password=hashed_password,
            email=signup_request.email
        )
        
        # Ajouter à la session et sauvegarder
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Pour récupérer l'ID généré
        
        # Créer le token
        token = create_jwt_token(new_user.id, new_user.username, new_user.email)
        
        return {
            "message": "Utilisateur créé avec succès",
            "username": new_user.username,
            "email": new_user.email,
            "token": token
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        print(f"Erreur register: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")