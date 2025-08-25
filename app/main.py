from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.version,
        debug=settings.debug,
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.debug else ["https://tudominio.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir routers
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def read_root():
        return {
            "message": f"Bienvenido a {settings.app_name}",
            "version": settings.version,
            "endpoints": {
                "categorias": "/api/v1/categorias",
                "materiales": "/api/v1/materiales",
                "puntos_reciclaje": "/api/v1/puntos-reciclaje",
                "buscar_puntos_cercanos": "/api/v1/puntos-reciclaje/cercanos?lat={lat}&lng={lng}&radio={km}",
            },
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
