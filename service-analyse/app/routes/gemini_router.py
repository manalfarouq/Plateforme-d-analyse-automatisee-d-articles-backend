from fastapi import APIRouter
from ..services.pipeline_service import analyser_texte_complet
from ..schemas.gemini_schema import TexteRequest

router = APIRouter()


@router.post("/analyser_gemini")
def analyser_texte(article: TexteRequest):
    """
    Analyse un texte : résumé + ton
    
    Exemple d'utilisation :
    POST /analyser
    {
        "texte": "Je veux un remboursement",
        "categorie": "service client"
    }
    """
    
    resultat = analyser_texte_complet(article.texte, article.categorie)
    
    return resultat