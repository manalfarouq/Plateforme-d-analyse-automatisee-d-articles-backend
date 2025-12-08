from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pathlib import Path   

# BASE_DIR = Path(__file__).resolve().parent.parent.parent   

class Settings(BaseSettings):
    """Configuration pour le service d'analyse"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Variable ANALYSE (obligatoire)
    HF_TOKEN: str
    
    # Variables optionnelles pour autres services
    SK: str = "not_needed"
    ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_HOST: str = "not_needed"
    DB_PORT: int = 5432
    DB_NAME: str = "not_needed"
    DB_USER: str = "not_needed"
    DB_PASSWORD: str = "not_needed"
    GEMINI_API_KEY: str = "not_needed"

settings = Settings()