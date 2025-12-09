from fastapi import FastAPI
from .routes import analyze_router, analyse_complet_router, gemini_router, history_router


app = FastAPI(title="Service d'Analyse d'Articles")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans le service d'analyse d'articles"}


app.include_router(analyze_router.router)  
app.include_router(analyse_complet_router.router)
# app.include_router(gemini_router.router)
app.include_router(history_router.router)

