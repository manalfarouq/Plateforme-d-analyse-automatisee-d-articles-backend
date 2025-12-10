# service-analyse/app/routes/filtrer_analyses_router.py

from fastapi import APIRouter, Query, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..database.db_connection import get_db
from ..models.analyse_log import AnalyseLog
from ..auth.token_auth import verify_token, get_user_id_from_token

router = APIRouter()


@router.get("/filtrer_analyses")
def filtrer_analyses(
    token: str = Header(...),
    categorie: Optional[str] = Query(None),
    ton: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Afficher l'historique des analyses de l'utilisateur connecté avec filtres optionnels
    """
    
    # 1. Vérifier le token et récupérer l'user_id
    verify_token(token)
    user_id = get_user_id_from_token(token)
    
    # 2. Construire la requête SQLAlchemy
    query = db.query(AnalyseLog).filter(AnalyseLog.user_id == user_id)
    
    # 3. Ajouter les filtres si présents
    if categorie:
        query = query.filter(AnalyseLog.categorie == categorie)
    
    if ton:
        query = query.filter(AnalyseLog.ton == ton)
    
    # 4. Exécuter la requête
    analyses = query.all()
    
    # 5. Transformer en JSON
    resultats = [
        {
            "id": analyse.id,
            "user_id": analyse.user_id,
            "texte_original": analyse.texte_original,
            "categorie": analyse.categorie,
            "resume": analyse.resume,
            "ton": analyse.ton,
        }
        for analyse in analyses
    ]
    
    return resultats