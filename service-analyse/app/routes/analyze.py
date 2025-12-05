from fastapi import APIRouter, Header, HTTPException
from app.services.huggingface_service import classifier_texte
from app.auth.token_auth import verify_token
from app.database.db_connection import get_db_connection
from app.schemas.TextRequest import TextRequest

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/AnalyzeText")
def analyze_text_endpoint(texte: TextRequest, token: str = Header(...)):
    """
    Endpoint pour analyser un texte en utilisant le service Hugging Face.
    Args:
        texte (TextRequest): Contient le texte et les catégories.
        token (str): Token JWT dans l'en-tête.
    Returns:
        dict: Résultat de la classification.
    """
    try:
        verify_token(token)
        resultat = classifier_texte(texte.text, texte.categorie)
        
        return {
            "success": True,
            "categorie": texte.categorie,
            "original_text": texte.text,
            "translated_text": resultat
        }
         
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )
