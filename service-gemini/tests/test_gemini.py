# service-gemini/tests/test_gemini.py

from app.services.gemini_service import generer_resume


def test_resume():
    """Test Gemini"""
    resultat = generer_resume("Test simple , j'aime utilise camera", "technologie")
    
    assert "resume" in resultat
    assert "ton" in resultat