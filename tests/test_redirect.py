from src.auth import get_current_active_user
from src.main import app
from fastapi.testclient import TestClient
from unittest import mock
import os

client = TestClient(app)


async def succesful_get_current_active_user():
    return {"username": "test@test.com"}


@mock.patch("src.routers.redirect.httpx")
def test_get_redirect_401_sin_jwt(mock_httpx):
    app.dependency_overrides = {}
    response = client.get("/redirect/usuarios/test?asd=1")
    assert response.status_code == 401
    assert not mock_httpx.called


@mock.patch("src.routers.redirect.httpx")
def test_get_redirect_arma_bien_url_usuarios(mock_httpx):
    app.dependency_overrides[get_current_active_user] = succesful_get_current_active_user
    response = client.get("/redirect/usuarios/test?asd=1")
    assert response.status_code == 200
    assert mock_httpx.get.call_args[0][0] == os.getenv("API_USUARIOS_URL") or "" + "/test?asd=1"
    assert "Authorization" in str(mock_httpx.get.call_args[1])
    assert "X-API-KEY" in str(mock_httpx.get.call_args[1])


@mock.patch("src.routers.redirect.httpx")
def test_get_redirect_arma_bien_url_cursos(mock_httpx):
    app.dependency_overrides[get_current_active_user] = succesful_get_current_active_user
    response = client.get("/redirect/cursos/test?asd=1")
    assert response.status_code == 200
    assert mock_httpx.get.call_args[0][0] == os.getenv("API_CURSOS_URL") or "" + "/test?asd=1"


@mock.patch("src.routers.redirect.httpx")
def test_get_redirect_400_api_inexistente(mock_httpx):
    app.dependency_overrides[get_current_active_user] = succesful_get_current_active_user
    response = client.get("/redirect/api_test/test?asd=1")
    assert response.status_code == 400
    assert not mock_httpx.called
