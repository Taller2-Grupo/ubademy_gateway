import httpx
import os

from src.schemas import UsuarioSchema


def get_user_by_username(username: str):
    return httpx.get(os.getenv("API_USUARIOS_URL") + f"/usuarios/{username}")


def create_user(usuario: UsuarioSchema.CreateUsuarioRequest):
    return httpx.post(os.getenv("API_USUARIOS_URL") + "/usuarios/add", json=usuario.dict())
