import psycopg2
from ..core.config import settings

def get_db_connection():
    """
    Crée et retourne une connexion à la base de données PostgreSQL.
    """
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