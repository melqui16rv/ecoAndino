from app.config.database import get_db_connection
from fastapi import HTTPException


class DatabaseService:
    def test_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    version = cur.fetchone()

                    # Contar registros en las tablas principales
                    cur.execute("SELECT COUNT(*) as total FROM categorias;")
                    categorias_count = cur.fetchone()["total"]

                    cur.execute("SELECT COUNT(*) as total FROM materiales;")
                    materiales_count = cur.fetchone()["total"]

                    cur.execute("SELECT COUNT(*) as total FROM puntos_reciclaje;")
                    puntos_count = cur.fetchone()["total"]

                    return {
                        "status": "success",
                        "database_version": version["version"],
                        "tables_count": {
                            "categorias": categorias_count,
                            "materiales": materiales_count,
                            "puntos_reciclaje": puntos_count,
                        },
                    }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
