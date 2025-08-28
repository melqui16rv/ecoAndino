from psycopg2.extras import RealDictCursor
from app.config.database import get_db_connection
from typing import List, Dict, Any, Optional
from app.schemas.material import MaterialResponse
from fastapi import HTTPException
from psycopg2 import IntegrityError


class MaterialRepository:
    def get_materiales(
        self, categoria_id: Optional[int] = None
    ) -> List[MaterialResponse]:
        """Obtener materiales, opcionalmente filtrados por categoría"""
        try:
            consulta = """
                        SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                        FROM materiales m
                        JOIN categorias c ON m.categoria_id = c.id
                        ORDER BY m.nombre;
                    """
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        consulta,
                        (categoria_id,),
                    )
                    resulado = cur.fetchall()
                    materiales = [MaterialResponse(**dict(row)) for row in resulado]
                    return materiales
        except Exception as e:
            raise Exception(f"Error al obtener materiales: {str(e)}")

    def get_material_by_categoria(
        self, categoria_id: int
    ) -> Optional[List[MaterialResponse]]:
        """Obtener materiales, opcionalmente filtrados por categoría"""
        try:
            consulta = """
                        SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                        FROM materiales m
                        JOIN categorias c ON m.categoria_id = c.id
                        WHERE m.categoria_id = %s
                        ORDER BY m.nombre;
                    """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(consulta, (categoria_id,))
                    resutlado = cur.fetchall()
                    conn.commit()
                    materiales = [MaterialResponse(**res) for res in resutlado]

                    return materiales

        except Exception as e:
            raise Exception(f"Error al obtener materiales: {str(e)}")

    def get_material_by_id(self, material_id: int) -> Optional[MaterialResponse]:
        """Obtener material por ID"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT m.*, c.nombre as categoria_nombre 
                        FROM materiales m 
                        JOIN categorias c ON m.categoria_id = c.id 
                        WHERE m.id = %s;
                    """,
                        (material_id,),
                    )
                    resultado = cur.fetchone()
                    material = (
                        MaterialResponse(**dict(resultado)) if resultado else None
                    )

                    return material
        except Exception as e:
            raise Exception(f"Error al obtener material: {str(e)}")

    def create_material(self, data: Dict[str, Any]) -> MaterialResponse:
        """Crear un nuevo material"""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        """
                        INSERT INTO materiales (nombre, codigo, descripcion, preparacion_requerida, beneficio_ambiental, requiere_manejo_especial, ejemplos, materiales_no_aceptados, es_peligroso, categoria_id, activo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                    """,
                        (
                            data.get("nombre"),
                            data.get("codigo"),
                            data.get("descripcion"),
                            data.get("preparacion_requerida"),
                            data.get("beneficio_ambiental"),
                            data.get("requiere_manejo_especial", False),
                            data.get("ejemplos"),
                            data.get("materiales_no_aceptados"),
                            data.get("es_peligroso", False),
                            data.get("categoria_id"),
                            data.get("activo", True),
                        ),
                    )
                    nuevo_material = cur.fetchone()
                    conn.commit()
                    return MaterialResponse(**nuevo_material)
        except Exception as e:
            raise Exception(f"Error al crear material: {str(e)}")

    def _build_update_query(self, campos_actualizados):
        campos = []
        valores = []
        for campo, valor in campos_actualizados.items():
            if valor is not None:
                campos.append(f"{campo} = %s")
                valores.append(valor)

        # Si no hay campos para actualizar, retornar None
        if not campos:
            return None, []

        consulta = f"""
            UPDATE materiales
            SET {", ".join(campos)}
            WHERE id = %s
            RETURNING id, nombre, codigo, descripcion, preparacion_requerida, 
                        beneficio_ambiental, requiere_manejo_especial, ejemplos, 
                        materiales_no_aceptados, es_peligroso, categoria_id, activo;
        """
        return consulta, valores

    def update_material(
        self, material_id: int, material_data: Dict[str, Any]
    ) -> Optional[MaterialResponse]:
        try:
            # Filtrar solo los campos que no son None (actualización parcial)
            campos_actualizados = {
                k: v for k, v in material_data.items() if v is not None
            }

            # Si no hay campos para actualizar, retornar el material actual
            if not campos_actualizados:
                return self.get_material_by_id(material_id)

            # Construir la query de actualización
            consulta, valores = self._build_update_query(campos_actualizados)
            if consulta is None:
                return self.get_material_by_id(material_id)

            # Agregar el material_id al final de los valores para el WHERE
            valores.append(material_id)

            # Ejecutar la consulta
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(consulta, valores)
                    resultado = cur.fetchone()
                    conn.commit()

                    if resultado:
                        return MaterialResponse(
                            id=resultado["id"],
                            nombre=resultado["nombre"],
                            codigo=resultado["codigo"],
                            descripcion=resultado["descripcion"],
                            preparacion_requerida=resultado["preparacion_requerida"],
                            beneficio_ambiental=resultado["beneficio_ambiental"],
                            requiere_manejo_especial=resultado[
                                "requiere_manejo_especial"
                            ],
                            ejemplos=resultado["ejemplos"],
                            materiales_no_aceptados=resultado[
                                "materiales_no_aceptados"
                            ],
                            es_peligroso=resultado["es_peligroso"],
                            categoria_id=resultado["categoria_id"],
                            activo=resultado["activo"],
                        )
                    return None

        except IntegrityError as e:
            if "materiales_nombre_key" in str(e):
                raise HTTPException(
                    status_code=409, detail="Ya existe un material con ese nombre"
                )
            if "materiales_codigo_key" in str(e):
                raise HTTPException(
                    status_code=409, detail="Ya existe un material con ese código"
                )
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(f"Error actualizando material: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    def delete_material(self, material_id: int) -> Optional[Dict[str, Any]]:
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Verificar si el material existe
                    cur.execute(
                        "SELECT id FROM materiales WHERE id = %s;", (material_id,)
                    )
                    if not cur.fetchone():
                        return None

                    # Eliminar el material
                    cur.execute(
                        "DELETE FROM materiales WHERE id = %s RETURNING id, nombre;",
                        (material_id,),
                    )
                    resultado = cur.fetchone()
                    conn.commit()

                    if resultado:
                        return {
                            "message": "Material eliminado exitosamente",
                            "material": {
                                "id": resultado["id"],
                                "nombre": resultado["nombre"],
                            },
                        }
                    return None
        except Exception as e:
            print(f"Error eliminando material: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")
