from collections import namedtuple
from unittest.mock import patch

import nest_asyncio
import pytest
from fastapi import HTTPException
from jose import jwt

from sample_fast_api.apps.auth.authentication import Token, authenticate_user, validate_token
from sample_fast_api.apps.users.schemas import pwd_context
from sample_fast_api.config import settings
from tests.apps.users.factories import UserFactory

nest_asyncio.apply()


def test_validate_token():
    encoded_jwt = jwt.encode({"sub": "username"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    assert validate_token(encoded_jwt) is None


def test_invalid_token():
    encoded_jwt = jwt.encode({"sub": "username"}, "invalid_secret_key", algorithm=settings.ALGORITHM)
    with pytest.raises(HTTPException) as exinfo:
        assert validate_token(encoded_jwt) is None
    assert exinfo.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
@patch("sample_fast_api.apps.auth.authentication.jwt.encode")
async def test_token_creation(mock_encode, client):
    mock_encode.return_value = "mock_hash"
    password_hash = pwd_context.hash("abc123")
    new_user = await UserFactory().create(name="username", password=password_hash)
    token = Token(new_user)
    assert token.create() == {"access_token": "mock_hash", "token_type": "bearer"}


@pytest.mark.asyncio
async def test_authenticate_user(client):
    password_hash = pwd_context.hash("abc123")
    new_user = await UserFactory().create(name="username", password=password_hash)

    RequestFormMock = namedtuple("OAuth2PasswordRequestForm", ["username", "password"])
    form_data = RequestFormMock("username", "abc123")
    user = await authenticate_user(form_data)
    assert user.id == new_user.id


@pytest.mark.asyncio
async def test_authenticate_user_ivalid_password(client):
    await UserFactory().create(name="username", password="unhased-password")

    RequestFormMock = namedtuple("OAuth2PasswordRequestForm", ["username", "password"])
    form_data = RequestFormMock("username", "abc123")
    with pytest.raises(HTTPException) as exinfo:
        await authenticate_user(form_data)
    assert "Incorrect username or password" == exinfo.value.detail


@pytest.mark.asyncio
async def test_authenticate_user_ivalid_username(client):
    password_hash = pwd_context.hash("abc123")
    await UserFactory().create(name="name", password=password_hash)

    RequestFormMock = namedtuple("OAuth2PasswordRequestForm", ["username", "password"])
    form_data = RequestFormMock("username", "abc123")
    with pytest.raises(HTTPException) as exinfo:
        await authenticate_user(form_data)
    assert "Incorrect username or password" == exinfo.value.detail
