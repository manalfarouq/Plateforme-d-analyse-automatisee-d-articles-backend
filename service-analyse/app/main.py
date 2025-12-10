# service-analyse/app/main.py

from fastapi import FastAPI
from .routes import (
    analyze_router,
    analyse_complet_router,
    history_router,
    filtrer_analyses_router
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Service d'Analyse d'Articles")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans le service d'analyse d'articles"}


app.include_router(analyze_router.router)
app.include_router(analyse_complet_router.router)
app.include_router(history_router.router)
app.include_router(filtrer_analyses_router.router)