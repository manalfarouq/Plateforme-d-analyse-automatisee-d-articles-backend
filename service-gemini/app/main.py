from fastapi import FastAPI
from .routes import gemini_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Service d'Analyse d'Articles avec Gemini")

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
    return {"message": "Bienvenue dans le service d'analyse d'articles avec Gemini"}


app.include_router(gemini_router.router)  