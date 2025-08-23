from app.repositories.punto_reciclaje_repository import PuntoReciclajeRepository
from app.repositories.material_repository import MaterialRepository
from app.config.settings import settings
from fastapi import HTTPException
from typing import List, Dict, Any, Optional


class PuntoReciclajeService:
    def __init__(self):
        self.punto_repo = PuntoReciclajeRepository()
        self.material_repo = MaterialRepository()

    def get_puntos_reciclaje(
        self, ciudad: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener puntos de reciclaje, opcionalmente filtrados por ciudad"""
        puntos = self.punto_repo.get_puntos_reciclaje(ciudad)
        return {"puntos_reciclaje": puntos}

    def get_puntos_cercanos(
        self, lat: float, lng: float, radio: Optional[float] = None
    ) -> Dict[str, Any]:
        """Buscar puntos de reciclaje cercanos a una ubicación"""
        if radio is None:
            radio = settings.default_search_radius

        puntos_cercanos = self.punto_repo.get_puntos_cercanos(lat, lng, radio)

        return {
            "ubicacion_busqueda": {"latitud": lat, "longitud": lng, "radio_km": radio},
            "puntos_encontrados": len(puntos_cercanos),
            "puntos": puntos_cercanos,
        }

    def get_materiales_por_punto(self, punto_id: int) -> Dict[str, Any]:
        """Obtener materiales que acepta un punto específico"""
        # Verificar que el punto existe
        punto = self.punto_repo.get_punto_by_id(punto_id)
        if not punto:
            raise HTTPException(
                status_code=404, detail="Punto de reciclaje no encontrado"
            )

        # Obtener materiales que acepta
        materiales = self.material_repo.get_materiales_por_punto(punto_id)

        return {
            "punto_reciclaje": punto,
            "total_materiales": len(materiales),
            "materiales_aceptados": materiales,
        }
