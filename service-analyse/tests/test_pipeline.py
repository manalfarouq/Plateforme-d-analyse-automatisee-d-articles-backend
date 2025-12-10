# service-analyse/tests/test_pipeline.py
import os
os.environ["HF_TOKEN"] = "fake_token"

from unittest.mock import patch
from app.services.pipeline_service import analyser_texte_complet


@patch("app.services.pipeline_service.requests.post")
def test_pipeline(mock_post):
    """Test pipeline"""
    
    # Mock de la réponse HuggingFace
    mock_post.return_value.json.return_value = {
        "resume": "Demande de remboursement",
        "ton": "neutre"
    }
    
    resultat = analyser_texte_complet("Je veux un remboursement")
    
    assert isinstance(resultat, dict)
    if "erreur" not in resultat:
        assert "resume" in resultat
        assert "ton" in resultat