# service-auth/app/models/__init__.py

from .user import Base, User
from .analyse_log import AnalyseLog

# Exporter tous les modèles
__all__ = ["Base", "User", "AnalyseLog"]


"""Solution avec __init__.py :

Charge User en premier
Charge AnalyseLog ensuite
SQLAlchemy peut maintenant résoudre la relation

C'est comme dire à Python : "Charge ces fichiers dans CET ordre précis" """