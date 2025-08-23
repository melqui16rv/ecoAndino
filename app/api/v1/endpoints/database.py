from fastapi import APIRouter
from app.services.database_service import DatabaseService

router = APIRouter()


@router.get("/test")
def test_database_connection():
    """Probar la conexión a la base de datos"""
    db_service = DatabaseService()
    return db_service.test_connection()
