# service-analyse/app/database/db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dépendance FastAPI pour obtenir une session SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()