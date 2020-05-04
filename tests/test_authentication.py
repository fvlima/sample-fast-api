import uuid

import pytest
from fastapi import HTTPException

from app.authentication import Authentication


def test_valid_authentication():
    token = f"Token {uuid.uuid4()}"
    auth = Authentication(token)

    assert auth


def test_invalid_authentication():
    with pytest.raises(HTTPException):
        Authentication("token")
