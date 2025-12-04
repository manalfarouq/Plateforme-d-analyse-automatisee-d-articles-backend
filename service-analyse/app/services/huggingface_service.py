import requests
from app.core.config import settings

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

def classifier_texte(texte, categories):
    """
    Classifie un texte selon des catégories.
    Args:
        texte (str): Le texte à classifier.
        categories (list): Liste des catégories possibles.
    Returns:
        dict: Résultat de la classification.
    """
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    
    donnees = {
        "inputs": texte,
        "parameters": {"candidate_labels": categories}
    }
    
    reponse = requests.post(API_URL, headers=headers, json=donnees)
    return reponse.json()


# test
# resultat = classifier_texte("Bonjour, j'ai récemment acheté un appareil mais il ne fonctionne pas. Je voudrais être remboursé!", ["remboursement", "legal"])
# print(resultat)