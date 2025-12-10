from fastapi import FastAPI
from .routes import login_router, register_router, get_all_users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Service d'Authentification avec JWT")


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans le service d'authentification avec JWT"}

app.include_router(login_router.router)
app.include_router(register_router.router)
app.include_router(get_all_users_router.router)