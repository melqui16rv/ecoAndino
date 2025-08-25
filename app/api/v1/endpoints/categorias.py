from fastapi import APIRouter
from sqlalchemy.util import ellipses_string
from app.services.categoria_service import CategoriaService
from fastapi import HTTPException

router = APIRouter()


@router.get("/")
def get_categorias():
    """Obtener todas las categorías de materiales"""
    categoria_service = CategoriaService()
    return categoria_service.get_all_categorias()


@router.get("/{categoria_id}")
def get_categoria(categoria_id: int):
    """Obtener una categoría de material por su ID"""
    categoria_service = CategoriaService()
    return categoria_service.get_categoria_by_id(categoria_id)


@router.post("/")
def create_categoria(categoria_data: dict):
    """Crear una nueva categoría de material"""
    if (
        categoria_data.get("nombre") is not None
        and categoria_data.get("descripcion") is not None
        and categoria_data.get("codigo") is not None
        and categoria_data.get("color_identificacion") is not None
        and categoria_data.get("icono") is not None
        and categoria_data.get("orden_display") is not None
        and categoria_data.get("activo") is not None
    ):
        categoria_service = CategoriaService()
        return categoria_service.create_categoria(categoria_data)
    else:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")


@router.patch("/{categoria_id}")
def update_categoria(categoria_id: int, categoria_data: dict):
    """Actualizar una categoría de material existente"""
    categoria_service = CategoriaService()
    if categoria_service.get_categoria_by_id(categoria_id) is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if not categoria_data:
        raise HTTPException(
            status_code=400, detail="No se proporcionaron datos para actualizar"
        )
    return categoria_service.update_categoria(categoria_id, categoria_data)


@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int):
    """Eliminar una categoría de material por su ID"""
    categoria_service = CategoriaService()
    if categoria_service.get_categoria_by_id(categoria_id) is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria_service.delete_categoria(categoria_id)
