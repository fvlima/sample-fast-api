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


class Token:
    def __init__(self, user):
        self.user = user

    def create(self):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": self.user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
