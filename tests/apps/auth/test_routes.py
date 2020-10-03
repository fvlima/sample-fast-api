import pytest
from fastapi import status

from sample_fast_api.apps.users.schemas import pwd_context
from tests.apps.users.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_payload",
    [
        {"username": "name", "password": "invalid-password"},
        {"username": "invalid-name", "password": "abc123"},
    ],
)
async def test_token_invalid_data(data_payload, client):
    password_hash = pwd_context.hash("abc123")
    await UserFactory().create(name="username", password=password_hash)
    response = client.post("/token", data=data_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


@pytest.mark.asyncio
async def test_token_success_creation(client):
    password_hash = pwd_context.hash("abc123")
    await UserFactory().create(name="name", password=password_hash)
    response = client.post("/token", data={"username": "name", "password": "abc123"})

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json().keys()
