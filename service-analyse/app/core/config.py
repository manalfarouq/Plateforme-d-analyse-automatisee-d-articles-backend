from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    # Variable ANALYSE
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
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()