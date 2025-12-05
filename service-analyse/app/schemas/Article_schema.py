from pydantic import BaseModel, Field

class ArticleAnalyzeRequest(BaseModel):
    """Schéma pour la requête d'analyse d'article"""
    text: str = Field(..., min_length=5, description="Contenu de l'article à analyser")
    
class ArticleAnalyzeResponse(BaseModel):
    """Schéma pour la réponse d'analyse"""
    summary: str
    sentiment: str
