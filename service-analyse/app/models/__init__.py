# service-analyse/app/models/__init__.py

from .user import Base, User
from .analyse_log import AnalyseLog

__all__ = ["Base", "User", "AnalyseLog"]