from pydantic import BaseModel
from typing import Optional
from datetime import time


class PuntoReciclajeBase(BaseModel):
    nombre: str
    direccion: str
    ciudad: str
    latitud: float
    longitud: float
    tipo_instalacion: str
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    estado: str = "activo"


class PuntoReciclajeResponse(PuntoReciclajeBase):
    id: int
    total_materiales_aceptados: Optional[int] = 0

    class Config:
        from_attributes = True


class PuntoCercanoResponse(PuntoReciclajeResponse):
    distancia_km: float


class UbicacionBusqueda(BaseModel):
    latitud: float
    longitud: float
    radio_km: float


class PuntosCercanosResponse(BaseModel):
    ubicacion_busqueda: UbicacionBusqueda
    puntos_encontrados: int
    puntos: list[PuntoCercanoResponse]
