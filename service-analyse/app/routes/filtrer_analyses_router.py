# service-analyse/app/routes/analyze_router.py

from fastapi import APIRouter, Query, Header, HTTPException
from typing import Optional
from ..database.db_connection import get_db_connection
from ..auth.token_auth import verify_token, get_user_id_from_token

router = APIRouter()


@router.get("/filtrer_analyses")
def filtrer_analyses(
    token: str = Header(...),
    categorie: Optional[str] = Query(None),
    ton: Optional[str] = Query(None),
):
    """
    Afficher l'historique des analyses de l'utilisateur connecté avec filtres optionnels
    """
    
    # 1. Vérifier le token et récupérer l'user_id
    verify_token(token)
    user_id = get_user_id_from_token(token)
    
    # 2. Construire la requête SQL
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, user_id, texte_original, categorie, resume, ton FROM analyse_logs WHERE user_id = %s"
    params = [user_id]
    
    # 3. Ajouter les filtres si l'utilisateur les a tapés
    if categorie:
        query += " AND categorie = %s"
        params.append(categorie)
    
    if ton:
        query += " AND ton = %s"
        params.append(ton)
    
    # 4. Exécuter la requête
    cursor.execute(query, tuple(params))
    analyses = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # 5. Transformer en JSON
    resultats = []
    for analyse in analyses:
        resultats.append({
            "id": analyse[0],
            "user_id": analyse[1],
            "texte_original": analyse[2],
            "categorie": analyse[3],
            "resume": analyse[4],
            "ton": analyse[5],
        })
    
    return resultats