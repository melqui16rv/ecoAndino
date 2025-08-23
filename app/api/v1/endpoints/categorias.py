from fastapi import APIRouter
from app.services.categoria_service import CategoriaService

router = APIRouter()


@router.get("/")
def get_categorias():
    """Obtener todas las categorías de materiales"""
    categoria_service = CategoriaService()
    return categoria_service.get_all_categorias()
