# service-auth/app/database/db_connection.py

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# Pour psycopg2 (actuel)
def get_db_connection():
    """Connexion PostgreSQL avec psycopg2"""
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    return conn


# Pour SQLAlchemy 
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dépendance FastAPI pour obtenir une session SQLAlchemy.
    Utilise yield pour fermer automatiquement la session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()