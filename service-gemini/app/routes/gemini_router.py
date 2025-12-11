# service-gemini/app/routes/gemini_router.py

from fastapi import APIRouter
from ..services.gemini_service import generer_resume
from ..schemas.gemini_schema import TexteRequest

router = APIRouter()

@router.post("/analyser_gemini")
def analyser_texte(article: TexteRequest):
    """
    Analyse un texte : résumé + ton
    """
    resultat = generer_resume(article.texte, article.categorie)
    return resultat
