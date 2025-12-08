# service-analyse/tests/test_analyse.py

from app.services.huggingface_service import classifier_articles


def test_classification():
    """Test HuggingFace"""
    resultat = classifier_articles("J'aime le sport")
    
    assert isinstance(resultat, list)
    assert len(resultat) > 0
    assert "label" in resultat[0]