from fastapi import APIRouter
from app.services.material_service import MaterialService
from typing import Optional

router = APIRouter()


@router.get("/")
def get_materiales(categoria_id: Optional[int] = None):
    """Obtener materiales, opcionalmente filtrados por categoría"""
    material_service = MaterialService()
    return material_service.get_materiales(categoria_id)


@router.get("/{material_id}/puntos")
def get_puntos_por_material(material_id: int):
    """Obtener puntos que aceptan un material específico"""
    material_service = MaterialService()
    return material_service.get_puntos_por_material(material_id)
