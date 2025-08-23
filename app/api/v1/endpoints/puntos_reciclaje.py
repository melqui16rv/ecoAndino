from fastapi import APIRouter
from app.services.punto_reciclaje_service import PuntoReciclajeService
from typing import Optional

router = APIRouter()


@router.get("/")
def get_puntos_reciclaje(ciudad: Optional[str] = None):
    """Obtener puntos de reciclaje, opcionalmente filtrados por ciudad"""
    punto_service = PuntoReciclajeService()
    return punto_service.get_puntos_reciclaje(ciudad)


@router.get("/cercanos")
def get_puntos_cercanos(lat: float, lng: float, radio: Optional[float] = None):
    """Buscar puntos de reciclaje cercanos a una ubicación"""
    punto_service = PuntoReciclajeService()
    return punto_service.get_puntos_cercanos(lat, lng, radio)


@router.get("/{punto_id}/materiales")
def get_materiales_por_punto(punto_id: int):
    """Obtener materiales que acepta un punto específico"""
    punto_service = PuntoReciclajeService()
    return punto_service.get_materiales_por_punto(punto_id)
