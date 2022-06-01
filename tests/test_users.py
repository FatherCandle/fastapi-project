from fastapi import status
from jose import jwt
import pytest
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserRes(**res.json())
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    # Data that was encoded at the creation of the token
    id = payload.get("user_id")

    assert res.status_code == status.HTTP_200_OK
    assert login_res.token_type == "bearer"
    assert id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("worngmail@gmail.com", "password123", 403),
        ("test123@gmail.com", "wrongpass", 403),
        ("worngmail@gmail.com", "wrongpass", 403),
        (None, "password123", 422),
        ("test123@gmail.com", None, 422),
    ],
)
def test_incorrect_login_user(client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code
