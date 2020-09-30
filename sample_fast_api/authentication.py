from typing import Optional
from datetime import timedelta, datetime
from uuid import UUID
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, status
from sample_fast_api.apps.users.models import User
from sample_fast_api.apps.users.schemas import pwd_context
from sample_fast_api.config import settings


class Authentication:
    def __init__(self, authorization: str = Header("")):
        token = authorization[6:]
        try:
            UUID(token)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")


async def authenticate_user(form_data):
    user = await User.query.where(User.name == form_data.username).gino.first()
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not user or not pwd_context.verify(form_data.password, user.password):
            raise exception
    except ValueError:
        raise exception
    return user


