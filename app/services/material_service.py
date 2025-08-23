from app.repositories.material_repository import MaterialRepository
from app.repositories.punto_reciclaje_repository import PuntoReciclajeRepository
from fastapi import HTTPException
from typing import List, Dict, Any, Optional


class MaterialService:
    def __init__(self):
        self.material_repo = MaterialRepository()
        self.punto_repo = PuntoReciclajeRepository()

    def get_materiales(
        self, categoria_id: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener materiales, opcionalmente filtrados por categoría"""
        materiales = self.material_repo.get_materiales(categoria_id)
        return {"materiales": materiales}

    def get_puntos_por_material(self, material_id: int) -> Dict[str, Any]:
        """Obtener puntos que aceptan un material específico"""
        # Verificar que el material existe
        material = self.material_repo.get_material_by_id(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material no encontrado")

        # Buscar puntos que aceptan este material
        puntos = self.punto_repo.get_puntos_por_material(material_id)

        return {
            "material": material,
            "total_puntos": len(puntos),
            "puntos_que_aceptan": puntos,
        }
