# service-gemini/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Variable principale
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()