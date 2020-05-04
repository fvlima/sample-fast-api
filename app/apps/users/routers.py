import typing
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select

from .schemas import User, UserCreate
from .tables import address as address_table
from .tables import user as user_table
from app.authentication import Authentication
from app.db_utils import insert_from_data
from app.pagination import Pagination

router = APIRouter()


@router.get(
    "/users/",
    description="Endpoint to search users",
    response_model=typing.List[User],
    dependencies=[Depends(Authentication)],
)
async def users_search(request: Request, p: Pagination = Depends()):
    query = select([user_table]).where(user_table.c.name == p.q).limit(p.limit).offset(p.offset)
    result = await request.state.db.fetch_all(query=query)

    return result


@router.get(
    "/users/{user_id}",
    description="Endpoint to fetch user",
    response_model=User,
    dependencies=[Depends(Authentication)],
)
async def users_get(user_id: UUID, request: Request, pagination: Pagination = Depends()):
    query = user_table.select().where(user_table.c.id == user_id)
    result = await request.state.db.fetch_one(query=query)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@router.post("/users/", dependencies=[Depends(Authentication)], response_model=User)
async def users_create(user: UserCreate, request: Request):
    async with request.state.db.transaction():
        user.password = user.hash_password()

        user_data = user.dict()
        address_data = user_data.pop("address")

        user.address.id = await insert_from_data(address_table, address_data, request.state.db)
        user_data["address_id"] = user.address.id
        user.id = await insert_from_data(user_table, user_data, request.state.db)

        return user
