# service-gemini/app/services/gemini_service.py

from google import genai
from ..core.config import settings
import json


def generer_resume(texte, categorie):
    """
    Gemini crée le résumé ET détecte le ton
    
    texte = le texte à résumer
    categorie = la catégorie
    """
    
    # Vérifier que la clé API est définie
    if not settings.GEMINI_API_KEY:
        return {
            "resume": None,
            "ton": None,
            "categorie": categorie,
            "erreur": "GEMINI_API_KEY non défini"
        }
    
    try:
        # Se connecter à Gemini
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Prompt pour résumé + ton
        prompt = f"""Analyse ce texte et donne-moi :
1. Un résumé COURT en 1 phrase maximum (15 mots max)
2. Le ton (positif, négatif ou neutre)

Texte : {texte}
Catégorie : {categorie}

Réponds UNIQUEMENT au format JSON comme ça :
{{
"resume": "ton résumé court ici",
"ton": "positif ou négatif ou neutre"
}}"""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        texte_reponse = response.text.strip()
        if "```json" in texte_reponse:
            texte_reponse = texte_reponse.replace("```json", "").replace("```", "")
        
        resultat = json.loads(texte_reponse)
        
        return {
            "resume": resultat.get("resume"),
            "ton": resultat.get("ton"),
            "categorie": categorie,
        }
    
    except Exception as e:
        return {
            "resume": None,
            "ton": None,
            "categorie": categorie,
            "erreur": str(e)
        }
