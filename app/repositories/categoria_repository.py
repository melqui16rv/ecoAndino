from app.config.database import get_db_connection
from typing import List, Dict, Any, Optional
from app.schemas.categoria import CategoriaResponse
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from psycopg2 import IntegrityError


class CategoriaRepository:
    def get_all_categorias(self) -> Optional[List[CategoriaResponse]]:
        """Obtener todas las categorías activas"""
        list_categorias: List[CategoriaResponse] = []
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo
                        FROM categorias
                        ORDER BY orden_display;
                    """)
                    rows = cur.fetchall()

                    if rows is None:
                        return None

                    for row in rows:
                        list_categorias.append(
                            CategoriaResponse(
                                id=row["id"],
                                nombre=row["nombre"],
                                descripcion=row["descripcion"],
                                codigo=row["codigo"],
                                color_identificacion=row["color_identificacion"],
                                icono=row["icono"],
                                orden_display=row["orden_display"],
                                activo=row["activo"],
                            )
                        )

            return list_categorias

        except Exception as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")

    def get_categoria_by_id(self, categoria_id: int) -> Optional[CategoriaResponse]:
        """Obtener una categoría específica por ID"""
        try:
            consulta = """
                    SELECT id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo
                    FROM categorias
                    WHERE id = %s;
                """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(consulta, (categoria_id,))
                    row = cur.fetchone()

                    if row is None:
                        return None

                    categoria = CategoriaResponse(
                        id=row["id"],
                        nombre=row["nombre"],
                        descripcion=row["descripcion"],
                        codigo=row["codigo"],
                        color_identificacion=row["color_identificacion"],
                        icono=row["icono"],
                        orden_display=row["orden_display"],
                        activo=row["activo"],
                    )
                    return categoria

        except Exception as e:
            raise Exception(
                f"Error al obtener categoría con ID {categoria_id}: {str(e)}"
            )

    def create_categoria(self, categoria_data: Dict[str, Any]) -> CategoriaResponse:
        """Crear una nueva categoría"""
        try:
            consulta = """
                INSERT INTO categorias (nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo;
            """

            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        consulta,
                        (
                            categoria_data["nombre"],
                            categoria_data.get("descripcion"),
                            categoria_data["codigo"],
                            categoria_data.get("color_identificacion"),
                            categoria_data.get("icono"),
                            categoria_data.get("orden_display", 0),
                            categoria_data.get("activo", True),
                        ),
                    )

                    new_row = cur.fetchone()
                    conn.commit()

                    if new_row is None:
                        return None

                    new_categoria = CategoriaResponse(
                        id=new_row["id"],
                        nombre=new_row["nombre"],
                        descripcion=new_row["descripcion"],
                        codigo=new_row["codigo"],
                        color_identificacion=new_row["color_identificacion"],
                        icono=new_row["icono"],
                        orden_display=new_row["orden_display"],
                        activo=new_row["activo"],
                    )

                    return new_categoria

        except Exception as e:
            raise Exception(f"Error al crear categoría: {str(e)}")

    def _build_update_query(self, campos_actualizados):
        campos = []
        valores = []

        for campo, valor in campos_actualizados.items():
            if valor is not None:  # Indentación corregida
                campos.append(f"{campo} = %s")
                valores.append(valor)

        # Si no hay campos para actualizar, retornar None
        if not campos:
            return None, []

        consulta = f"""
                UPDATE categorias
                SET {", ".join(campos)}
                WHERE id = %s
                RETURNING id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo;
            """
        return consulta, valores

    def update_categoria(
        self, categoria_id: int, categoria_data: Dict[str, Any]
    ) -> Optional[CategoriaResponse]:
        try:
            # Filtrar solo los campos que no son None (actualización parcial)
            campos_actualizados = {
                k: v for k, v in categoria_data.items() if v is not None
            }

            # Si no hay campos para actualizar, retornar la categoría actual
            if not campos_actualizados:
                return self.get_categoria_by_id(categoria_id)

            # Construir la query de actualización
            consulta, valores = self._build_update_query(campos_actualizados)

            if consulta is None:
                return self.get_categoria_by_id(categoria_id)

            # Agregar el categoria_id al final de los valores para el WHERE
            valores.append(categoria_id)

            # Ejecutar la consulta

            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(consulta, valores)
                    resultado = cur.fetchone()
                    conn.commit()

                    if resultado:
                        return CategoriaResponse(
                            id=resultado["id"],
                            nombre=resultado["nombre"],
                            descripcion=resultado["descripcion"],
                            codigo=resultado["codigo"],
                            color_identificacion=resultado["color_identificacion"],
                            icono=resultado["icono"],
                            orden_display=resultado["orden_display"],
                            activo=resultado["activo"],
                        )

                    return None
        except IntegrityError as e:
            if "categorias_nombre_key" in str(e):
                raise HTTPException(
                    status_code=409, detail="Ya existe una categoría con ese nombre"
                )
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            print(f"Error actualizando categoría: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    def delete_categoria(self, categoria_id: int) -> Optional[Dict[str, Any]]:
        """Eliminar una categoría por su ID"""
        try:
            consulta = "DELETE FROM categorias Where id=%s"
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(consulta, (categoria_id,))
                    conn.commit()
                    if cur.rowcount == 0:
                        raise HTTPException(
                            status_code=404, detail="Categoría no encontrada"
                        )
                    return {
                        "status": "success",
                        "id": categoria_id,
                        "detail": "Categoría eliminada exitosamente",
                    }

        except Exception as e:
            print(f"Error actualizando categoría: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
