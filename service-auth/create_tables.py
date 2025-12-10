# service-auth/create_tables.py

from app.models import Base, User, AnalyseLog
from app.database.db_connection import engine

# Créer toutes les tables
Base.metadata.create_all(bind=engine)
print("Tables créées avec succès !")