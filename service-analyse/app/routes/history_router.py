# service-analyse/app/routes/history_router.py

from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from ..auth.token_auth import verify_token, get_user_id_from_token
from ..database.db_connection import get_db
from ..models.analyse_log import AnalyseLog

router = APIRouter()


@router.get("/history")
def get_user_history(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des analyses de l'utilisateur
    """
    try:
        verify_token(token)
        user_id = get_user_id_from_token(token)
        
        # Récupérer les analyses avec SQLAlchemy
        analyses = db.query(AnalyseLog)\
            .filter(AnalyseLog.user_id == user_id)\
            .limit(50)\
            .all()
        
        # Formater les résultats
        historique = [
            {
                "id": analyse.id,
                "texte_original": analyse.texte_original,
                "categorie": analyse.categorie,
                "resume": analyse.resume,
                "ton": analyse.ton,
            }
            for analyse in analyses
        ]
        
        return {
            "success": True,
            "count": len(historique),
            "historique": historique
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur récupération historique: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de l'historique")