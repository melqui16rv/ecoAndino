from app.repositories.material_repository import MaterialRepository
from app.repositories.punto_reciclaje_repository import PuntoReciclajeRepository
from fastapi import HTTPException
from typing import List, Dict, Any, Optional

from app.schemas.material import MaterialResponse


class MaterialService:
    def __init__(self):
        self.material_repo = MaterialRepository()
        self.punto_repo = PuntoReciclajeRepository()

    def get_materiales(
        self, categoria_id: Optional[int] = None
    ) -> List[MaterialResponse]:
        """Obtener materiales, opcionalmente filtrados por categoría"""
        materiales = self.material_repo.get_materiales(categoria_id)
        return materiales

    def get_materiales_por_categoria(self, categoria_id: int) -> List[MaterialResponse]:
        """Obtener materiales por categoría"""
        materiales = self.material_repo.get_material_by_categoria(categoria_id)
        if not materiales:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron materiales para la categoría proporcionada",
            )
        return materiales

    def get_material_by_id(self, material_id: int) -> MaterialResponse:
        """Obtener puntos que aceptan un material específico"""
        # Verificar que el material existe
        material = self.material_repo.get_material_by_id(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material no encontrado")

        return material

    def create_material(self, data: Dict[str, Any]) -> MaterialResponse:
        """Crear un nuevo material"""
        try:
            if "categoria_id" not in data:
                raise HTTPException(
                    status_code=400, detail="El campo 'categoria_id' es obligatorio"
                )

            nuevo_material = self.material_repo.create_material(data)
            return nuevo_material
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error al crear material: {str(e)}"
            )

    def update_material(
        self, material_id: int, data: Dict[str, Any]
    ) -> Optional[MaterialResponse]:
        """Actualizar un material existente"""
        try:
            # Verificar que el material existe
            material_existente = self.material_repo.get_material_by_id(material_id)
            if not material_existente:
                raise HTTPException(status_code=404, detail="Material no encontrado")

            material_actualizado = self.material_repo.update_material(material_id, data)
            return material_actualizado
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error al actualizar material: {str(e)}"
            )

    def delete_material(self, material_id: int) -> Optional[Dict[str, Any]]:
        """Eliminar un material existente"""
        try:
            # Verificar que el material existe
            material_existente = self.material_repo.get_material_by_id(material_id)
            if not material_existente:
                raise HTTPException(status_code=404, detail="Material no encontrado")

            # Verificar si el material está asociado a algún punto de reciclaje
            puntos_asociados = self.punto_repo.get_puntos_por_material(material_id)
            if puntos_asociados:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar el material porque está asociado a uno o más puntos de reciclaje",
                )

            resultado = self.material_repo.delete_material(material_id)
            return resultado

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error al eliminar material: {str(e)}"
            )
