from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .authentication import Token, authenticate_user

router = APIRouter()


@router.post("/auth/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data)
    token = Token(user)
    return token.create()


def include_router(app):
    app.include_router(router)
