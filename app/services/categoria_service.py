from app.repositories.categoria_repository import CategoriaRepository
from typing import List, Dict, Any


class CategoriaService:
    def __init__(self):
        self.categoria_repo = CategoriaRepository()

    def get_all_categorias(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener todas las categorías"""
        categorias = self.categoria_repo.get_all_categorias()
        return {"categorias": categorias}
