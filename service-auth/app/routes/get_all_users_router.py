# service-auth/app/routes/get_all_users_router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.db_connection import get_db
from ..models.user import User
from ..auth.token_auth import verify_token

router = APIRouter()


@router.get("/GetAllUsers")
def get_all_users(
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Endpoint pour récupérer tous les utilisateurs avec SQLAlchemy.
    """
    try:
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalide")

        # Récupérer tous les utilisateurs
        users = db.query(User).all()

        return {
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
                for user in users
            ]
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Erreur GetAllUsers: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des utilisateurs")