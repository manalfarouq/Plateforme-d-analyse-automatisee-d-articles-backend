# service-analyse/app/routes/history_router.py

from fastapi import APIRouter, Header, HTTPException
from ..auth.token_auth import verify_token, get_user_id_from_token
from ..database.db_connection import get_db_connection

router = APIRouter()


@router.get("/history")
def get_user_history(token: str = Header(...)):
    """
    Récupère l'historique des analyses de l'utilisateur
    """
    try:
        verify_token(token)
        user_id = get_user_id_from_token(token)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, texte_original, categorie, resume, ton, created_at
            FROM analyse_logs
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 50
        """, (user_id,))
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Formater les résultats
        historique = []
        for row in rows:
            historique.append({
                "id": row[0],
                "texte_original": row[1],
                "categorie": row[2],
                "resume": row[3],
                "ton": row[4],
                "created_at": row[5].isoformat() if row[5] else None
            })
        
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