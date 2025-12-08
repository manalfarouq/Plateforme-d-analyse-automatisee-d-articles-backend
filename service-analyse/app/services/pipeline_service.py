# service-analyse/app/services/pipeline_service.py

import requests
from .huggingface_service import classifier_articles

GEMINI_SERVICE_URL = "http://localhost:8001/analyser_gemini"


def analyser_texte_complet(texte):
    """Pipeline : HuggingFace → Gemini"""
    
    # Étape 1 : Classification
    resultat_hf = classifier_articles(texte)
    
    if not isinstance(resultat_hf, list) or len(resultat_hf) == 0:
        return {"erreur": "Erreur classification"}
    
    categorie = resultat_hf[0]["label"]
    score = resultat_hf[0]["score"]
    
    # Étape 2 : Appel Gemini
    try:
        response = requests.post(
            GEMINI_SERVICE_URL,
            json={"texte": texte, "categorie": categorie},
            timeout=30
        )
        resultat_gemini = response.json()
        
        if "erreur" in resultat_gemini:
            return {"erreur": "Erreur Gemini"}
        
        return {
            "classification": {"categorie": categorie, "score": score},
            "resume": resultat_gemini["resume"],
            "ton": resultat_gemini["ton"]
        }
    
    except:
        return {"erreur": "Service Gemini indisponible"}