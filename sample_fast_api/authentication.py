from uuid import UUID

from fastapi import Header, HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication:
    def __init__(self, authorization: str = Header("")):
        token = authorization[6:]
        try:
            UUID(token)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
