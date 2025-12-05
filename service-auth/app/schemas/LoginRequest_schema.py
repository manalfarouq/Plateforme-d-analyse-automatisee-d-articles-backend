from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(...,description="Nom d'utilisateur")
    password: str = Field(...,description="Mot de passe")