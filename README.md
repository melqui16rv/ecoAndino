# Proyecto FastAPI

Estructura básica para iniciar un proyecto con FastAPI.

## Estructura
- `main.py`: Punto de entrada de la aplicación FastAPI.
- `app/`: Carpeta para módulos y rutas de la aplicación.
- `requirements.txt`: Dependencias necesarias (FastAPI y Uvicorn).

## Cómo ejecutar
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```
3. Accede a la API en [http://localhost:8000](http://localhost:8000)
