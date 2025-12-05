from fastapi import APIRouter, HTTPException, Header
from ..database.db_connection import get_db_connection
from ..core.config import settings
from jose import jwt

router = APIRouter()

@router.get("/GetAllUsers")
def get_all_users(token: str = Header(...)):
    """
    Endpoint pour récupérer tous les utilisateurs.
    Args:
        token (str): Token JWT dans l'en-tête.
    Returns:
        list: Liste des utilisateurs.
    """
    conn = None
    cursor = None

    try:
        # Vérifier le token JWT
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        user_id = payload.get("sub")  # sub contient user_id

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalide")

        # Connexion DB
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer tous les utilisateurs sans la colonne role
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()

        return {
            "users": [
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2]  
                }
                for user in users
            ]
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Le token a expiré")

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    except Exception as e:
        # Log l'erreur mais message générique pour l'utilisateur
        print(f"Erreur GetAllUsers: {str(e)}")  
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la récupération des utilisateurs"
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()