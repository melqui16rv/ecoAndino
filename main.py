from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="EcoAndino API", description="API para gestión de reciclaje", version="1.0.0")

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función helper para conexión directa con psycopg2
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a EcoAndino API",
        "version": "1.0.0",
        "endpoints": {
            "categorias": "/categorias",
            "materiales": "/materiales",
            "puntos_reciclaje": "/puntos-reciclaje",
            "buscar_puntos_cercanos": "/puntos-cercanos?lat={lat}&lng={lng}&radio={km}"
        }
    }

@app.get("/test-db")
def test_database_connection():
    """Probar la conexión a la base de datos"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                
                # Contar registros en las tablas principales
                cur.execute("SELECT COUNT(*) as total FROM categorias;")
                categorias_count = cur.fetchone()['total']
                
                cur.execute("SELECT COUNT(*) as total FROM materiales;")
                materiales_count = cur.fetchone()['total']
                
                cur.execute("SELECT COUNT(*) as total FROM puntos_reciclaje;")
                puntos_count = cur.fetchone()['total']
                
                return {
                    "status": "success",
                    "database_version": version['version'],
                    "tables_count": {
                        "categorias": categorias_count,
                        "materiales": materiales_count,
                        "puntos_reciclaje": puntos_count
                    }
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")

@app.get("/categorias")
def get_categorias():
    """Obtener todas las categorías de materiales"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nombre, descripcion, codigo, color_identificacion, icono, orden_display, activo
                    FROM categorias 
                    WHERE activo = true 
                    ORDER BY orden_display;
                """)
                categorias = cur.fetchall()
                return {"categorias": categorias}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

@app.get("/materiales")
def get_materiales(categoria_id: Optional[int] = None):
    """Obtener materiales, opcionalmente filtrados por categoría"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                if categoria_id:
                    cur.execute("""
                        SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                        FROM materiales m
                        JOIN categorias c ON m.categoria_id = c.id
                        WHERE m.categoria_id = %s AND m.activo = true
                        ORDER BY m.nombre;
                    """, (categoria_id,))
                else:
                    cur.execute("""
                        SELECT m.*, c.nombre as categoria_nombre, c.color_identificacion, c.icono
                        FROM materiales m
                        JOIN categorias c ON m.categoria_id = c.id
                        WHERE m.activo = true
                        ORDER BY c.orden_display, m.nombre;
                    """)
                materiales = cur.fetchall()
                return {"materiales": materiales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener materiales: {str(e)}")

@app.get("/puntos-reciclaje")
def get_puntos_reciclaje(ciudad: Optional[str] = None):
    """Obtener puntos de reciclaje, opcionalmente filtrados por ciudad"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                if ciudad:
                    cur.execute("""
                        SELECT p.*, COUNT(pm.material_id) as total_materiales_aceptados
                        FROM puntos_reciclaje p
                        LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
                        WHERE p.ciudad ILIKE %s AND p.estado = 'activo'
                        GROUP BY p.id
                        ORDER BY p.nombre;
                    """, (f"%{ciudad}%",))
                else:
                    cur.execute("""
                        SELECT p.*, COUNT(pm.material_id) as total_materiales_aceptados
                        FROM puntos_reciclaje p
                        LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
                        WHERE p.estado = 'activo'
                        GROUP BY p.id
                        ORDER BY p.ciudad, p.nombre;
                    """)
                puntos = cur.fetchall()
                return {"puntos_reciclaje": puntos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener puntos de reciclaje: {str(e)}")

@app.get("/puntos-cercanos")
def get_puntos_cercanos(lat: float, lng: float, radio: float = 10.0):
    """Buscar puntos de reciclaje cercanos a una ubicación"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
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
                """, (lat, lng, lat, lat, lng, lat, radio))
                puntos_cercanos = cur.fetchall()
                return {
                    "ubicacion_busqueda": {"latitud": lat, "longitud": lng, "radio_km": radio},
                    "puntos_encontrados": len(puntos_cercanos),
                    "puntos": puntos_cercanos
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar puntos cercanos: {str(e)}")

@app.get("/material/{material_id}/puntos")
def get_puntos_por_material(material_id: int):
    """Obtener puntos que aceptan un material específico"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Primero verificar que el material existe
                cur.execute("""
                    SELECT m.*, c.nombre as categoria_nombre 
                    FROM materiales m 
                    JOIN categorias c ON m.categoria_id = c.id 
                    WHERE m.id = %s AND m.activo = true;
                """, (material_id,))
                material = cur.fetchone()
                
                if not material:
                    raise HTTPException(status_code=404, detail="Material no encontrado")
                
                # Buscar puntos que aceptan este material
                cur.execute("""
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
                """, (material_id,))
                puntos = cur.fetchall()
                
                return {
                    "material": material,
                    "total_puntos": len(puntos),
                    "puntos_que_aceptan": puntos
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar puntos para el material: {str(e)}")

@app.get("/punto/{punto_id}/materiales")
def get_materiales_por_punto(punto_id: int):
    """Obtener materiales que acepta un punto específico"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Verificar que el punto existe
                cur.execute("""
                    SELECT * FROM puntos_reciclaje WHERE id = %s AND estado = 'activo';
                """, (punto_id,))
                punto = cur.fetchone()
                
                if not punto:
                    raise HTTPException(status_code=404, detail="Punto de reciclaje no encontrado")
                
                # Obtener materiales que acepta
                cur.execute("""
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
                """, (punto_id,))
                materiales = cur.fetchall()
                
                return {
                    "punto_reciclaje": punto,
                    "total_materiales": len(materiales),
                    "materiales_aceptados": materiales
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener materiales del punto: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
