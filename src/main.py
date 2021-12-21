from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import (
    OAuth2PasswordRequestForm
)
from jose import jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from src.auth import User, get_user, Token, get_current_active_user
from src.schemas import UsuarioSchema
from dotenv import load_dotenv
import pyrebase
from src.external_services.api_usuarios_external_service\
    import create_user, post_evento_login_credenciales, post_evento_login_google
from src.routers import redirect


# TODO: Repetidos en auth.py
SECRET_KEY = "6120898dcf1ef5f1b3e46e745d0cfdd1d9733042b24fa239617a9b4419d32253"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180


config = {
  "apiKey": "AIzaSyAN9QKyNRt236PAj2r4Axn-Kvc0iZFdIUM",
  "authDomain": "ubademy-grupo7.firebaseapp.com",
  "databaseURL": "https://ubademy-grupo7-default-rtdb.firebaseio.com/",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)

load_dotenv()


class UserInDB(User):
    password: str
    esAdmin: bool


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(redirect.router)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    scopes: List[str] = []

    if user.esAdmin:
        scopes.append("admin")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expires_delta=access_token_expires
    )
    post_evento_login_credenciales()

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/usuarios/registrar", response_model=UsuarioSchema.UsuarioResponse)
async def registrar_usuario(usuario: UsuarioSchema.CreateUsuarioRequest):
    usuario.password = get_password_hash(usuario.password)
    response = create_user(usuario)
    if response.json().get("success") == "true":
        return response.json().get("data")
    error = response.json().get("error")
    raise HTTPException(status_code=response.status_code, detail=error)


@app.get("/token/swap/{firebase_token}")
async def swap_token(firebase_token: str):
    data = firebase.auth().get_account_info(firebase_token)
    mail = data["users"][0]["email"]
    user = get_user(mail)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    post_evento_login_google()

    return {"access_token": access_token, "token_type": "bearer"}


# Para debuguear:
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
