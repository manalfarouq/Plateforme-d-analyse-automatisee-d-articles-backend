from fastapi import FastAPI
from app.routes import analyze

app = FastAPI(title="Application d'analyse des Arcticles avec Authentification JWT")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans l'API d'analyse des Articles avec JWT"}


app.include_router(analyze.router)  