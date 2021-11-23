from fastapi import APIRouter, HTTPException, Depends, Header, Request
import httpx
from typing import Optional

from src.auth import User, get_current_active_user

router = APIRouter(
    prefix="/redirect",
    tags=["redirect"]
)


def get_api_url(api):
    if api == "usuarios":
        return "https://ubademy-usuarios.herokuapp.com"

    if api == "cursos":
        return "https://ubademy-back.herokuapp.com"

    raise HTTPException(400, "Nombre de API incorrecto.")


@router.get("/{api_name}/{rest_of_path:path}")
async def redirect_get(
        api_name: str,
        rest_of_path: str,
        current_user: User = Depends(get_current_active_user),
        authorization: Optional[str] = Header(None)):
    api_url = get_api_url(api_name)
    headers = {"Authorization": authorization}
    return httpx.get(f"{api_url}/{rest_of_path}", headers=headers).json()


@router.post("/{api_name}/{rest_of_path:path}")
async def redirect_post(
        api_name: str,
        rest_of_path: str,
        request: Request,
        current_user: User = Depends(get_current_active_user),
        authorization: Optional[str] = Header(None)):
    api_url = get_api_url(api_name)
    headers = {"Authorization": authorization}
    body = await request.json()
    return httpx.post(f"{api_url}/{rest_of_path}", headers=headers, json=body).json()


@router.delete("/{api_name}/{rest_of_path:path}")
async def redirect_delete(
        api_name: str,
        rest_of_path: str,
        current_user: User = Depends(get_current_active_user),
        authorization: Optional[str] = Header(None)):
    api_url = get_api_url(api_name)
    headers = {"Authorization": authorization}
    return httpx.delete(f"{api_url}/{rest_of_path}", headers=headers).json()


@router.put("/{api_name}/{rest_of_path:path}")
async def redirect_put(
        api_name: str,
        rest_of_path: str,
        request: Request,
        current_user: User = Depends(get_current_active_user),
        authorization: Optional[str] = Header(None)):
    api_url = get_api_url(api_name)
    headers = {"Authorization": authorization}
    body = await request.json()
    return httpx.put(f"{api_url}/{rest_of_path}", headers=headers, json=body).json()


@router.patch("/{api_name}/{rest_of_path:path}")
async def redirect_patch(
        api_name: str,
        rest_of_path: str,
        request: Request,
        current_user: User = Depends(get_current_active_user),
        authorization: Optional[str] = Header(None)):
    api_url = get_api_url(api_name)
    headers = {"Authorization": authorization}
    body = await request.json()
    return httpx.patch(f"{api_url}/{rest_of_path}", headers=headers, json=body).json()
