from pydantic import BaseModel

class TexteRequest(BaseModel):
    texte: str
    categorie: str