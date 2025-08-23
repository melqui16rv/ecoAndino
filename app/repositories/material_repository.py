from app.config.database import get_db_connection
from typing import List, Dict, Any, Optional


class MaterialRepository:
    def get_materiales(
        self, categoria_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtener materiales, opcionalmente filtrados por categoría"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    if categoria_id:
                        cur.execute(
                            """
                            SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                            FROM materiales m
                            JOIN categorias c ON m.categoria_id = c.id
                            WHERE m.categoria_id = %s AND m.activo = true
                            ORDER BY m.nombre;
                        """,
                            (categoria_id,),
                        )
                    else:
                        cur.execute("""
                            SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                            FROM materiales m
                            JOIN categorias c ON m.categoria_id = c.id
                            WHERE m.activo = true
                            ORDER BY c.orden_display, m.nombre;
                        """)
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener materiales: {str(e)}")

    def get_material_by_id(self, material_id: int) -> Optional[Dict[str, Any]]:
        """Obtener material por ID"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT m.*, c.nombre as categoria_nombre 
                        FROM materiales m 
                        JOIN categorias c ON m.categoria_id = c.id 
                        WHERE m.id = %s AND m.activo = true;
                    """,
                        (material_id,),
                    )
                    return cur.fetchone()
        except Exception as e:
            raise Exception(f"Error al obtener material: {str(e)}")

    def get_materiales_por_punto(self, punto_id: int) -> List[Dict[str, Any]]:
        """Obtener materiales que acepta un punto específico"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 
                            m.id,
                            m.nombre,
                            m.codigo,
                            m.descripcion,
                            m.preparacion_requerida,
                            m.es_peligroso,
                            c.nombre as categoria_nombre,
                            c.color_identificacion,
                            c.icono,
                            pm.observaciones,
                            pm.cantidad_maxima,
                            pm.horario_especial
                        FROM materiales m
                        JOIN categorias c ON m.categoria_id = c.id
                        JOIN punto_materiales pm ON m.id = pm.material_id
                        WHERE pm.punto_reciclaje_id = %s AND pm.acepta = true AND m.activo = true
                        ORDER BY c.orden_display, m.nombre;
                    """,
                        (punto_id,),
                    )
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener materiales del punto: {str(e)}")
