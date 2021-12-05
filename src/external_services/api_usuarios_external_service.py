import httpx
import os

from src.schemas import UsuarioSchema


def get_user_by_username(username: str):
    headers = {"X-API-KEY": os.getenv("API_USUARIOS_KEY")}
    return httpx.get(os.getenv("API_USUARIOS_URL") + f"/usuarios/{username}", headers=headers)


def create_user(usuario: UsuarioSchema.CreateUsuarioRequest):
    headers = {"X-API-KEY": os.getenv("API_USUARIOS_KEY")}
    return httpx.post(os.getenv("API_USUARIOS_URL") + "/usuarios/add", json=usuario.dict(), headers=headers)
