from fastapi import FastAPI
from .routes import gemini_router

app = FastAPI(title="Service d'Analyse d'Articles avec Gemini")


@app.get("/")
async def root():
    return {"message": "Bienvenue dans le service d'analyse d'articles avec Gemini"}


app.include_router(gemini_router.router)  