# service-analyse/tests/test_pipeline.py

from app.services.pipeline_service import analyser_texte_complet


def test_pipeline():
    """Test pipeline"""
    resultat = analyser_texte_complet("Je veux un remboursement")
    
    assert isinstance(resultat, dict)
    if "erreur" not in resultat:
        assert "resume" in resultat
        assert "ton" in resultat