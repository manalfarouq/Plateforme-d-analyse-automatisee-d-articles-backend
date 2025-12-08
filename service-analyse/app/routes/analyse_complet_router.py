# service-analyse/app/routes/analyse_complet_router.py

from fastapi import APIRouter, Header, HTTPException
from ..auth.token_auth import verify_token 
from ..schemas.Article_schema import ArticleAnalyzeRequest
from ..services.pipeline_service import analyser_texte_complet

router = APIRouter()


@router.post("/AnalyzeComplet")
def analyze_complet_endpoint(articles: ArticleAnalyzeRequest, token: str = Header(...)):
    """
    Pipeline complet HuggingFace + Gemini
    """
    try:
        verify_token(token)
        
        resultat = analyser_texte_complet(articles.text)
        
        # Vérifier si erreur
        if "erreur" in resultat:
            raise HTTPException(status_code=500, detail=resultat["erreur"])
        
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