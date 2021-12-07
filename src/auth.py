from typing import Optional, List
from jose import jwt, JWTError
from fastapi import Security, HTTPException, Depends, status
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from pydantic import BaseModel, ValidationError
from src.external_services.api_usuarios_external_service import get_user_by_username
from src.schemas import UsuarioSchema


# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "6120898dcf1ef5f1b3e46e745d0cfdd1d9733042b24fa239617a9b4419d32253"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Privilegios de admin."}
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str


def get_user(username: str):
    response = get_user_by_username(username)

    if response.status_code == 404:
        raise HTTPException(404, "Usuario no encontrado")

    if response.json().get('data').get('estado') != 'activo':
        raise HTTPException(403, "Usuario no se encuentra activo")

    usuario = UsuarioSchema.UsuarioResponse.parse_obj(response.json().get("data"))
    return usuario


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user)
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
