from pydantic import BaseModel
from typing import Optional


class MaterialBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    preparacion_requerida: Optional[str] = None
    es_peligroso: bool = False
    categoria_id: int
    activo: bool = True


class MaterialResponse(MaterialBase):
    id: int
    categoria_nombre: Optional[str] = None
    color_identificacion: Optional[str] = None
    icono: Optional[str] = None

    class Config:
        from_attributes = True
