from pydantic import BaseModel, Field, EmailStr

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nom d'utilisateur")
    email: EmailStr = Field(..., description="Adresse email")
    password: str = Field(..., min_length=4, description="Mot de passe")