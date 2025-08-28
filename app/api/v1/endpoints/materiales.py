from fastapi import APIRouter
from app.services.material_service import MaterialService
from typing import Optional

router = APIRouter()


@router.get("/")
def get_materiales(categoria_id: Optional[int] = None):
    """Obtener materiales, opcionalmente filtrados por categoría"""
    material_service = MaterialService()
    return material_service.get_materiales(categoria_id)


@router.get("/categoria/{categoria_id}")
def get_materiales_por_categoria(categoria_id: int):
    """Obtener materiales por categoría"""
    material_service = MaterialService()
    return material_service.get_materiales_por_categoria(categoria_id)


@router.get("/{material_id}")
def get_puntos_por_material(material_id: int):
    """Obtener puntos que aceptan un material específico"""
    material_service = MaterialService()
    return material_service.get_material_by_id(material_id)


@router.post("/")
def create_material(data: dict):
    """Crear un nuevo material"""
    material_service = MaterialService()
    return material_service.create_material(data)


@router.patch("/{material_id}")
def update_material(material_id: int, data: dict):
    """Actualizar un material existente"""
    material_service = MaterialService()
    return material_service.update_material(material_id, data)


@router.delete("/{material_id}")
def delete_material(material_id: int):
    """Eliminar un material"""
    material_service = MaterialService()
    return material_service.delete_material(material_id)
