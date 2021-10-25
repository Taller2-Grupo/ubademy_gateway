import datetime
from typing import Optional
from pydantic import BaseModel, validator
from fastapi import HTTPException


class UsuarioBase(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    esAdmin = False


# En esta clase se le agregan todos los atributos particulares para la creación
class CreateUsuarioRequest(UsuarioBase):
    @validator('username')
    def tiene_username(cls, username: str):
        if not username:
            raise HTTPException(status_code=400, detail='Debe proporcionar un username.')
        return username

    @validator('password')
    def tiene_password(cls, password: str):
        if not password:
            raise HTTPException(status_code=400, detail='Debe proporcionar una password.')
        return password

    @validator('nombre')
    def tiene_nombre(cls, nombre: str):
        if not nombre:
            raise HTTPException(status_code=400, detail='Debe proporcionar un nombre.')
        return nombre

    @validator('apellido')
    def tiene_apellido(cls, apellido: str):
        if not apellido:
            raise HTTPException(status_code=400, detail='Debe proporcionar un apellido.')
        return apellido


# Esto es lo que se va a devolver cuando se este "leyendo" un Usuario
class UsuarioResponse(UsuarioBase):
    id: int
    fechaCreacion: datetime.datetime
    fechaActualizacion: Optional[datetime.datetime]
