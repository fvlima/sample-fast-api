import uuid
from collections import namedtuple
from fastapi import HTTPException
import nest_asyncio
import pytest
from fastapi import HTTPException

from sample_fast_api.apps.users.schemas import pwd_context
from sample_fast_api.authentication import Authentication, authenticate_user
from tests.apps.users.factories import UserFactory

nest_asyncio.apply()


def test_valid_authentication():
    token = f"Token {uuid.uuid4()}"
    auth = Authentication(token)

    assert auth


def test_invalid_authentication():
    with pytest.raises(HTTPException):
        Authentication("token")


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
