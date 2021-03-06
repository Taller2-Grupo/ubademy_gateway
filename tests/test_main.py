from src.main import app
from fastapi.testclient import TestClient
from unittest import mock

client = TestClient(app)


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.post_evento_login_credenciales")
def test_token_usuario_existe_password_correcta(mock_post_evento, mock_get_user_by_username):
    mock_get_user_by_username.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "28",
                    "username": "l@gmail.com",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "Cosme",
                    "apellido": "Fulanito",
                    "esAdmin": "true",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "activo"
                }
            }
        })
    response = client.post("/token", data={"username": "l@gmail.com", "password": "string"})
    assert response.status_code == 200


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.post_evento_login_credenciales")
def test_token_usuario_existe_password_incorrecta(mock_post_evento, mock_get_user_by_username):
    mock_get_user_by_username.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "28",
                    "username": "l@gmail.com",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "Cosme",
                    "apellido": "Fulanito",
                    "esAdmin": "true",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "activo"
                }
            }
        })
    response = client.post("/token", data={"username": "l@gmail.com", "password": "string2"})
    assert response.status_code == 400


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.post_evento_login_credenciales")
def test_token_usuario_existe_estado_bloqueado(mock_post_evento, mock_get_user_by_username):
    mock_get_user_by_username.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "28",
                    "username": "l@gmail.com",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "Cosme",
                    "apellido": "Fulanito",
                    "esAdmin": "true",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "bloqueado"
                }
            }
        })
    response = client.post("/token", data={"username": "l@gmail.com", "password": "string2"})
    assert response.status_code == 403


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.post_evento_login_credenciales")
def test_token_usuario_inexistente(mock_post_evento, mock_get_user_by_username):
    mock_get_user_by_username.return_value = mock.Mock(**{"status_code": 404})
    response = client.post("/token", data={"username": "string", "password": "string"})
    assert response.status_code == 404


@mock.patch("src.main.create_user")
def test_register(mock_create_user):
    mock_create_user.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "1",
                    "username": "test",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "test",
                    "apellido": "test",
                    "esAdmin": "false",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "activo"
                }
            }
        })
    response = client.post(
        "/usuarios/registrar",
        json={
            "username": "test",
            "password": "string",
            "nombre": "test",
            "apellido": "test",
            "esAdmin": "false"
        })
    assert response.status_code == 200


@mock.patch("src.main.create_user")
def test_register_existing_user(mock_create_user):
    mock_create_user.return_value = mock.Mock(
        **{
            "status_code": 400,
            "json.return_value": {
                "success": "false",
                "error": "Ya existe el usuario"
            }
        })
    response = client.post(
        "/usuarios/registrar",
        json={
            "username": "test",
            "password": "string",
            "nombre": "test",
            "apellido": "test",
            "esAdmin": "false"
        })
    assert response.status_code == 400
    assert response.json().get("detail") == "Ya existe el usuario"


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.firebase")
@mock.patch("src.main.post_evento_login_google")
def test_swap_token_user_existe(mock_post_evento, mock_firebase, mock_get_user_by_username):
    mock_firebase.return_value = mock.Mock(
        **{
            "auth.return_value.get_account_info.return_value": {
                    "users": [{"email": "l@gmail.com"}]
            }
        }
    )
    mock_get_user_by_username.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "28",
                    "username": "l@gmail.com",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "Cosme",
                    "apellido": "Fulanito",
                    "esAdmin": "true",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "activo"
                }
            }
        })
    response = client.get("/token/swap/qwerty")
    assert response.status_code == 200


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.firebase")
@mock.patch("src.main.post_evento_login_google")
def test_swap_token_user_existe_estado_bloqueado(mock_post_evento, mock_firebase, mock_get_user_by_username):
    mock_firebase.return_value = mock.Mock(
        **{
            "auth.return_value.get_account_info.return_value": {
                    "users": [{"email": "l@gmail.com"}]
            }
        }
    )
    mock_get_user_by_username.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "success": "true",
                "data": {
                    "id": "28",
                    "username": "l@gmail.com",
                    "password": "$2b$12$9iS3whvq.k.zzDDoU41WQuDbEkQtFTaqGR/j3BMKx6phmWdasbJt.",
                    "nombre": "Cosme",
                    "apellido": "Fulanito",
                    "esAdmin": "true",
                    "fechaCreacion": "2021-11-05T19:39:54.669Z",
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z",
                    "estado": "bloqueado"
                }
            }
        })
    response = client.get("/token/swap/qwerty")
    assert response.status_code == 403


@mock.patch("src.auth.get_user_by_username")
@mock.patch("src.main.firebase")
@mock.patch("src.main.post_evento_login_google")
def test_swap_token_user_no_existe(mock_post_evento, mock_firebase, mock_get_user_by_username):
    mock_firebase.return_value = mock.Mock(
        **{
            "auth.return_value.get_account_info.return_value": {
                    "users": [{"email": "l@gmail.com"}]
            }
        }
    )
    mock_get_user_by_username.return_value = mock.Mock(**{"status_code": 404})
    response = client.get("/token/swap/qwerty")
    assert response.status_code == 404
