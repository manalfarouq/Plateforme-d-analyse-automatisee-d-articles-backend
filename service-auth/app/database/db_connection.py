import psycopg2
from app.core.config import settings

"""
Qu'est-ce que ça fait ?

=> Cette fonction crée une connexion entre Python et PostgreSQL
=> C'est comme ouvrir une porte entre le code et la base de données
=> Chaque fois que je veux lire/écrire dans la base, j'appelle cette fonction
"""

def get_db_connection():

    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    return conn

# Utiliser DATABASE_URL si disponible (Render)
    # database_url = os.getenv("DATABASE_URL")