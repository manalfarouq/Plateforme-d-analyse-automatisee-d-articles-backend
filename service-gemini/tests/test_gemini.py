# service-gemini/tests/test_gemini.py

from unittest.mock import patch
from app.services.gemini_service import generer_resume


def test_resume():
    """Test Gemini avec mock"""
    
    # Réponse mockée
    mock_response = {
        "resume": "Test de résumé généré",
        "ton": "technologie"
    }
    
    # Mock de la fonction generer_resume
    with patch('app.services.gemini_service.generer_resume', return_value=mock_response):
        resultat = generer_resume("Test simple , j'aime utilise camera", "technologie")
        
        assert "resume" in resultat
        assert "ton" in resultat