from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Base de datos
    database_url: str = os.getenv("DATABASE_URL")

    # Configuración de la aplicación
    app_name: str = "EcoAndino API"
    app_description: str = "API para gestión de reciclaje"
    version: str = "1.0.0"
    debug: bool = False

    # Configuración de búsqueda
    default_search_radius: float = 10.0

    class Config:
        env_file = ".env"


settings = Settings()
