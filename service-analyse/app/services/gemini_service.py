# service-gemini/app/services/gemini_service.py

from google import genai
from ..core.config import settings
import json


def generer_resume(texte, categorie):
    """
    Gemini crée le résumé ET détecte le ton
    
    texte = le texte à résumer
    categorie = la catégorie trouvée par HuggingFace
    """
    
    try:
        # Se connecter à Gemini
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Demander à Gemini de faire résumé + ton
        prompt = f"""Analyse ce texte et donne-moi :
            1. Un résumé COURT en 1 phrase maximum (15 mots max)
            2. Le ton (positif, négatif ou neutre)

            Texte : {texte}
            Catégorie : {categorie}

            IMPORTANT : Le résumé doit être TRÈS COURT et direct.

            Réponds UNIQUEMENT au format JSON comme ça :
            {{
            "resume": "ton résumé court ici",
            "ton": "positif ou négatif ou neutre"
            }}"""
        
        # Demander à Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Récupérer la réponse
        texte_reponse = response.text.strip()
        
        # Enlever les ``` si Gemini les ajoute
        if "```json" in texte_reponse:
            texte_reponse = texte_reponse.replace("```json", "").replace("```", "")
        
        # Transformer en objet Python
        resultat = json.loads(texte_reponse)
        
        return {
            "resume": resultat["resume"],
            "ton": resultat["ton"],
            "categorie": categorie,
        }
    
    except Exception as e:
        # Si erreur
        return {
            "resume": None,
            "ton": None,
            "categorie": categorie,
            "erreur": str(e)
        }

