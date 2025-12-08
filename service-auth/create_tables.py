from app.models.user import Base
from app.models.analyse_log import AnalyseLog 
from sqlalchemy import create_engine
from app.core.config import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
print("Tables créées !")