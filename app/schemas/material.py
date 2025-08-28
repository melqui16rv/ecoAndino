from pydantic import BaseModel
from typing import Optional


class MaterialBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    preparacion_requerida: Optional[str] = None
    beneficio_ambiental: Optional[str] = None
    requiere_manejo_especial: Optional[bool] = False
    ejemplos: Optional[str] = None
    materiales_no_aceptados: Optional[str] = None
    es_peligroso: bool = False
    categoria_id: int
    activo: bool = True


class MaterialResponse(MaterialBase):
    id: int

    class Config:
        from_attributes = True
