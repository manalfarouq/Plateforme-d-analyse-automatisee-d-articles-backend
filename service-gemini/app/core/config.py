from pydantic_settings import BaseSettings
from pathlib import Path   

BASE_DIR = Path(__file__).resolve().parent.parent.parent   

class Settings(BaseSettings):
    # Variable GEMINI
    GEMINI_API_KEY: str
    
    # Variables optionnelles pour autres services
    SK: str = "not_needed"
    ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_HOST: str = "not_needed"
    DB_PORT: int = 5432
    DB_NAME: str = "not_needed"
    DB_USER: str = "not_needed"
    DB_PASSWORD: str = "not_needed"
    HF_TOKEN: str = "not_needed"
    
    class Config:
        env_file = ".env"

settings = Settings()