# service-analyse/app/routes/analyse_complet_router.py

from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from ..auth.token_auth import verify_token, get_user_id_from_token
from ..schemas.Article_schema import ArticleAnalyzeRequest
from ..services.pipeline_service import analyser_texte_complet
from ..database.db_connection import get_db
from ..models.analyse_log import AnalyseLog

router = APIRouter()


@router.post("/AnalyzeComplet")
def analyze_complet_endpoint(
    articles: ArticleAnalyzeRequest,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
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
        
        # SAUVEGARDE EN BASE DE DONNÉES avec SQLAlchemy
        try:
            nouvelle_analyse = AnalyseLog(
                user_id=user_id,
                texte_original=articles.text,
                categorie=resultat["classification"]["categorie"],
                resume=resultat["resume"],
                ton=resultat["ton"]
            )
            
            db.add(nouvelle_analyse)
            db.commit()
            db.refresh(nouvelle_analyse)
            
            print(f"Analyse sauvegardée avec ID: {nouvelle_analyse.id}")
            
        except Exception as e:
            db.rollback()
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