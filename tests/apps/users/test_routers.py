import uuid

import nest_asyncio
import pytest
from fastapi import status

from .factories import UserFactory
from sample_fast_api.apps.users.models import User as UserModel

# because the http test client runs an event loop fot itself,
# this lib is necessary to avoid the errror "this event loop
# is already running"
nest_asyncio.apply()


@pytest.fixture
def user_id():
    return str(uuid.uuid4())


def test_create(client, user_data):
    response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()

    assert user["id"]
    assert user["name"] == user_data["name"]
    assert user["email"] == user_data["email"]
    assert user["is_active"] == user_data["is_active"]
    assert user["permissions"] == user_data["permissions"]

    address = user["address"]

    assert address["city"] == user_data["address"]["city"]
    assert address["country"] == user_data["address"]["country"]
    assert address["number"] == user_data["address"]["number"]
    assert address["postal_code"] == user_data["address"]["postal_code"]
    assert address["state"] == user_data["address"]["state"]
    assert address["street"] == user_data["address"]["street"]


def test_create_missing_required_field(client, user_data):
    user_data.pop("name")
    response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update(client, user_data):
    user = await UserFactory.create()
    user_data["name"] = "John Doe"

    response = client.put(f"/users/{user.id}", json=user_data)
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user["name"] == "John Doe"


@pytest.mark.asyncio
async def test_update_missing_required_field(client, user_data):
    user = await UserFactory.create()
    user_data.pop("name")

    response = client.put(f"/users/{user.id}", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_not_found(client, user_id, user_data):
    response = client.put(f"/users/{user_id}", json=user_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get(client, user_data):
    user = await UserFactory.create()

    response = client.get(f"/users/{user.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"]
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["is_active"] == user_data["is_active"]
    assert data["permissions"] == user_data["permissions"]

    data = data["address"]

    assert data["city"] == user_data["address"]["city"]
    assert data["country"] == user_data["address"]["country"]
    assert data["number"] == user_data["address"]["number"]
    assert data["postal_code"] == user_data["address"]["postal_code"]
    assert data["state"] == user_data["address"]["state"]
    assert data["street"] == user_data["address"]["street"]


def test_get_not_found(client, user_id):
    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_search(client, user_data):
    user = await UserFactory.create()

    response = client.get(f"/users/?q={user.name}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_search_with_pagination_limit_offset(client, user_data):
    await UserFactory.create()
    await UserFactory.create()

    user_name = user_data["name"]
    response = client.get(f"/users/?q={user_name}&limit=1&offset=0")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert len(await UserModel.query.gino.all()) == 2


def test_search_without_results(client):
    response = client.get("/users/?name=Some Name")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_delete(client, user_data):
    user = await UserFactory.create()

    response = client.delete(f"/users/{user.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_found(client, user_id):
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
