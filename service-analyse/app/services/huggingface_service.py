import requests
from ..core.config import settings

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

def classifier_articles(texte, categories=None): 
    """
    Classifie un texte selon des catégories.
    Args:
        texte (str): Le texte à classifier.
        categories (list, optional): Liste des catégories possibles.
    Returns:
        dict: Résultat de la classification.
    """
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    
    # Catégories par défaut si non fournies
    if categories is None:
        categories = ["technologie", "politique", "sport", "économie", "santé", "service client", "remboursement"]
    
    donnees = {
        "inputs": texte,
        "parameters": {"candidate_labels": categories}
    }
    
    try:
        reponse = requests.post(API_URL, headers=headers, json=donnees, timeout=30)
        reponse.raise_for_status()
        return reponse.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur API HuggingFace: {str(e)}")
        return {"error": str(e)}


# test
# resultat = classifier_articles("je veux remborcer")
# print(resultat)