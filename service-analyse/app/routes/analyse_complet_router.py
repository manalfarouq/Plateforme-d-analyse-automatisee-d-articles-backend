# service-analyse/app/routes/analyse_complet_router.py

from fastapi import APIRouter, Header, HTTPException
from ..auth.token_auth import verify_token, get_user_id_from_token
from ..schemas.Article_schema import ArticleAnalyzeRequest
from ..services.pipeline_service import analyser_texte_complet
from ..database.db_connection import get_db_connection
from ..auth.token_auth import verify_token, get_user_id_from_token

router = APIRouter()


@router.post("/AnalyzeComplet")
def analyze_complet_endpoint(articles: ArticleAnalyzeRequest, token: str = Header(...)):
    """
    Pipeline complet HuggingFace + Gemini + Sauvegarde BDD
    """
    try:
        # Vérification du token
        verify_token(token)
        user_id = get_user_id_from_token(token)
        
        # Analyse du texte
        resultat = analyser_texte_complet(articles.text)
        
        # Vérifier si erreur
        if "erreur" in resultat:
            raise HTTPException(status_code=500, detail=resultat["erreur"])
        
        # SAUVEGARDE EN BASE DE DONNÉES
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analyse_logs (user_id, texte_original, categorie, resume, ton)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                user_id,
                articles.text,
                resultat["classification"]["categorie"],
                resultat["resume"],
                resultat["ton"]
            ))
            
            analyse_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Analyse sauvegardée avec ID: {analyse_id}")
            
        except Exception as e:
            print(f"Erreur sauvegarde BDD: {e}")
            # On continue même si la sauvegarde échoue
        
        # Retour du résultat
        return {
            "success": True,
            "original_text": articles.text,
            "classification": {
                "categorie": resultat["classification"]["categorie"],
                "score": f"{resultat['classification']['score'] * 100:.2f}%"
            },
            "resume": resultat["resume"],
            "ton": resultat["ton"]
        }
         
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"Erreur pipeline: {str(e)}") 
        raise HTTPException(status_code=500, detail="Erreur lors de l'analyse complète")