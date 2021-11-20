from src.main import app
from fastapi.testclient import TestClient
from unittest import mock

client = TestClient(app)


@mock.patch("src.main.get_user_by_username")
def test_token_usuario_existe_password_correcta(mock_get_user_by_username):
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
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z"
                }
            }
        })
    response = client.post("/token", data={"username": "l@gmail.com", "password": "string"})
    assert response.status_code == 200


@mock.patch("src.main.get_user_by_username")
def test_token_usuario_inexistente(mock_get_user_by_username):
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
                    "fechaActualizacion": "2021-11-06T00:00:00.000Z"
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
