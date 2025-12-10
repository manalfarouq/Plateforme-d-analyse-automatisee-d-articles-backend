from fastapi import APIRouter
from ..services.gemini_service import generer_resume
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
    
    resultat = generer_resume(article.texte, article.categorie)
    
    return resultat