from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    codigo: str
    color_identificacion: Optional[str] = None
    icono: Optional[str] = None
    orden_display: int
    activo: bool = True


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
