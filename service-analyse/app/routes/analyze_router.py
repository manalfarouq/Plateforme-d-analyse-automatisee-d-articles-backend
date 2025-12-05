from fastapi import APIRouter, Header, HTTPException
from ..services.huggingface_service import classifier_articles
from ..auth.token_auth import verify_token 
from ..database.db_connection import get_db_connection
from ..schemas.Article_schema import ArticleAnalyzeRequest

router = APIRouter()

@router.post("/AnalyzeText")
def analyze_text_endpoint(articles: ArticleAnalyzeRequest, token: str = Header(...)):
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
            meilleure_categorie = resultat[0]  # Le premier élément a le score le plus élevé
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