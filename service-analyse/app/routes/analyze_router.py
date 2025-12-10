# service-analyse/app/routes/analyze_router.py

from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from ..services.huggingface_service import classifier_articles
from ..auth.token_auth import verify_token
from ..schemas.Article_schema import ArticleAnalyzeRequest
from ..database.db_connection import get_db

router = APIRouter()


@router.post("/AnalyzeText")
def analyze_text_endpoint(
    articles: ArticleAnalyzeRequest,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint pour analyser un article en utilisant le service Hugging Face.
    Args:
        articles (ArticleAnalyzeRequest): Contient le texte de l'article.
        token (str): Token JWT dans l'en-tête.
    Returns:
        dict: Résultat de la classification (meilleure catégorie uniquement).
    """
    try:
        verify_token(token)
        resultat = classifier_articles(articles.text)
        
        # Extraire uniquement la catégorie avec le score le plus élevé
        if isinstance(resultat, list) and len(resultat) > 0:
            meilleure_categorie = resultat[0]
            meilleure_categorie["score"] = f"{meilleure_categorie['score'] * 100:.2f}%"
        else:
            meilleure_categorie = resultat
        
        return {
            "success": True,
            "original_text": articles.text,
            "best_category": meilleure_categorie
        }
         
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"Erreur analyse: {str(e)}") 
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'analyse de l'article"
        )