from app.repositories.categoria_repository import CategoriaRepository
from typing import List, Optional, Any, Dict
from app.schemas.categoria import CategoriaResponse


class CategoriaService:
    def __init__(self):
        self.categoria_repo = CategoriaRepository()

    def get_all_categorias(self) -> Optional[List[CategoriaResponse]]:
        """Obtener todas las categorías"""
        categorias = self.categoria_repo.get_all_categorias()
        return categorias

    def get_categoria_by_id(self, categoria_id: int) -> Optional[CategoriaResponse]:
        categoria = self.categoria_repo.get_categoria_by_id(categoria_id=categoria_id)
        return categoria

    def create_categoria(self, categoria_data: dict) -> CategoriaResponse:
        nueva_categoria = self.categoria_repo.create_categoria(
            categoria_data=categoria_data
        )
        return nueva_categoria

    def update_categoria(
        self, categoria_id: int, categoria_data: dict
    ) -> Optional[CategoriaResponse]:
        categoria_actualizada = self.categoria_repo.update_categoria(
            categoria_id=categoria_id, categoria_data=categoria_data
        )
        return categoria_actualizada

    def delete_categoria(self, categoria_id: int) -> Optional[Dict[str, Any]]:
        resultado = self.categoria_repo.delete_categoria(categoria_id=categoria_id)
        return resultado
