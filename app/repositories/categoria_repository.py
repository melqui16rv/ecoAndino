from app.config.database import get_db_connection
from typing import List, Dict, Any


class CategoriaRepository:
    def get_all_categorias(self) -> List[Dict[str, Any]]:
        """Obtener todas las categorías activas"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo
                        FROM categorias 
                        WHERE activo = true 
                        ORDER BY orden_display;
                    """)
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")
