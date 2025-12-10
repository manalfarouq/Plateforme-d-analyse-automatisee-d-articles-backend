# service-analyse/tests/test_analyse.py
import os
os.environ["HF_TOKEN"] = "fake_token"

from unittest.mock import patch
from app.services.huggingface_service import classifier_articles


@patch("app.services.huggingface_service.requests.post")
def test_classification(mock_post):
    """Test HuggingFace"""
    
    mock_post.return_value.json.return_value = [{"label": "SPORT", "score": 0.95}]
    
    resultat = classifier_articles("J'aime le sport")
    
    assert isinstance(resultat, list)
    assert len(resultat) > 0
    assert "label" in resultat[0]
    assert resultat[0]["label"] == "SPORT"
    assert resultat[0]["score"] > 0.5