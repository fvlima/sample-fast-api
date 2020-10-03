import typing
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from .models import Address as AddressModel
from .models import User as UserModel
from .schemas import User, UserCreate
from sample_fast_api.apps.auth.authentication import validate_token
from sample_fast_api.main import db
from sample_fast_api.pagination import Pagination

router = APIRouter()


@router.get(
    "/users/",
    description="Endpoint to search users",
    response_model=typing.List[User],
    dependencies=[Depends(validate_token)],
)
async def users_search(p: Pagination = Depends()):
    query = UserModel.join(AddressModel).select().where(UserModel.name == p.q).limit(p.limit).offset(p.offset)
    users = await query.gino.load(UserModel.load(address=AddressModel)).all()

    return users


@router.get(
    "/users/{user_id}",
    description="Endpoint to fetch user",
    response_model=User,
    dependencies=[Depends(validate_token)],
)
async def users_get(user_id: UUID):
    query = UserModel.join(AddressModel).select().where(UserModel.id == user_id)
    user = await query.gino.load(UserModel.load(address=AddressModel)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post(
    "/users/",
    dependencies=[Depends(validate_token)],
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def users_create(user: UserCreate):
    async with db.transaction():
        address = await AddressModel.create(
            city=user.address.city,
            complement=user.address.complement,
            country=user.address.country,
            number=user.address.number,
            postal_code=user.address.postal_code,
            state=user.address.state,
            street=user.address.street,
        )

        user = await UserModel.create(
            name=user.name,
            email=user.email,
            password=user.hash_password(),
            is_active=user.is_active,
            permissions=user.permissions,
            address_id=address.id,
        )

        user.address = address
        return user


@router.put("/users/{user_id}", dependencies=[Depends(validate_token)], response_model=User)
async def users_update(user_id: UUID, user: User):
    async with db.transaction():
        user_ = await UserModel.get_or_404(user_id)

        await AddressModel.update.values(
            city=user.address.city,
            complement=user.address.complement,
            country=user.address.country,
            number=user.address.number,
            postal_code=user.address.postal_code,
            state=user.address.state,
            street=user.address.street,
        ).where(AddressModel.id == user_.address_id).gino.status()

        await user_.update(
            name=user.name, email=user.email, is_active=user.is_active, permissions=user.permissions
        ).apply()

        user.id = user_.id
        user.address.id = user_.address_id
        return user


@router.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validate_token)]
)
async def users_delete(user_id: UUID):
    async with db.transaction():
        user = await UserModel.get_or_404(user_id)
        address = await AddressModel.get(user.address_id)

        await user.delete()
        await address.delete()


def include_router(app):
    app.include_router(router)
