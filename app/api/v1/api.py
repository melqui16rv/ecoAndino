from fastapi import APIRouter
from app.api.v1.endpoints import categorias, materiales, puntos_reciclaje, database

api_router = APIRouter()

api_router.include_router(database.router, prefix="/database", tags=["database"])
api_router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
api_router.include_router(materiales.router, prefix="/materiales", tags=["materiales"])
api_router.include_router(
    puntos_reciclaje.router, prefix="/puntos-reciclaje", tags=["puntos-reciclaje"]
)
