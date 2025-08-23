from app.config.database import get_db_connection
from typing import List, Dict, Any, Optional


class PuntoReciclajeRepository:
    def get_puntos_reciclaje(
        self, ciudad: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtener puntos de reciclaje, opcionalmente filtrados por ciudad"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    if ciudad:
                        cur.execute(
                            """
                            SELECT p.*, COUNT(pm.material_id) as total_materiales_aceptados
                            FROM puntos_reciclaje p
                            LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
                            WHERE p.ciudad ILIKE %s AND p.estado = 'activo'
                            GROUP BY p.id
                            ORDER BY p.nombre;
                        """,
                            (f"%{ciudad}%",),
                        )
                    else:
                        cur.execute("""
                            SELECT p.*, COUNT(pm.material_id) as total_materiales_aceptados
                            FROM puntos_reciclaje p
                            LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
                            WHERE p.estado = 'activo'
                            GROUP BY p.id
                            ORDER BY p.ciudad, p.nombre;
                        """)
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener puntos de reciclaje: {str(e)}")

    def get_puntos_cercanos(
        self, lat: float, lng: float, radio: float
    ) -> List[Dict[str, Any]]:
        """Buscar puntos de reciclaje cercanos a una ubicación"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 
                            p.id,
                            p.nombre,
                            p.direccion,
                            p.ciudad,
                            p.latitud,
                            p.longitud,
                            p.tipo_instalacion,
                            p.horario_apertura,
                            p.horario_cierre,
                            p.telefono,
                            p.email,
                            ROUND(
                                CAST(
                                    6371 * acos(
                                        cos(radians(%s)) * 
                                        cos(radians(p.latitud)) * 
                                        cos(radians(p.longitud) - radians(%s)) + 
                                        sin(radians(%s)) * 
                                        sin(radians(p.latitud))
                                    ) AS DECIMAL
                                ), 2
                            ) as distancia_km,
                            COUNT(pm.material_id) as total_materiales
                        FROM puntos_reciclaje p
                        LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
                        WHERE p.estado = 'activo'
                        AND (
                            6371 * acos(
                                cos(radians(%s)) * 
                                cos(radians(p.latitud)) * 
                                cos(radians(p.longitud) - radians(%s)) + 
                                sin(radians(%s)) * 
                                sin(radians(p.latitud))
                            )
                        ) <= %s
                        GROUP BY p.id, p.nombre, p.direccion, p.ciudad, p.latitud, p.longitud, p.tipo_instalacion, p.horario_apertura, p.horario_cierre, p.telefono, p.email
                        ORDER BY distancia_km;
                    """,
                        (lat, lng, lat, lat, lng, lat, radio),
                    )
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al buscar puntos cercanos: {str(e)}")

    def get_punto_by_id(self, punto_id: int) -> Optional[Dict[str, Any]]:
        """Obtener punto por ID"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT * FROM puntos_reciclaje WHERE id = %s AND estado = 'activo';
                    """,
                        (punto_id,),
                    )
                    return cur.fetchone()
        except Exception as e:
            raise Exception(f"Error al obtener punto: {str(e)}")

    def get_puntos_por_material(self, material_id: int) -> List[Dict[str, Any]]:
        """Obtener puntos que aceptan un material específico"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 
                            p.id,
                            p.nombre,
                            p.direccion,
                            p.ciudad,
                            p.latitud,
                            p.longitud,
                            p.tipo_instalacion,
                            p.horario_apertura,
                            p.horario_cierre,
                            p.telefono,
                            pm.observaciones,
                            pm.cantidad_maxima,
                            pm.horario_especial
                        FROM puntos_reciclaje p
                        JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id
                        WHERE pm.material_id = %s AND pm.acepta = true AND p.estado = 'activo'
                        ORDER BY p.ciudad, p.nombre;
                    """,
                        (material_id,),
                    )
                    return cur.fetchall()
        except Exception as e:
            raise Exception(f"Error al buscar puntos para el material: {str(e)}")
