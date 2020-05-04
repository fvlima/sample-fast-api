import pytest


@pytest.fixture
def address_data():
    return {
        "id": "3cdac50e-f31b-483d-bf00-c6dffc439393",
        "city": "City",
        "complement": "",
        "country": "Country",
        "number": "9999",
        "postal_code": "00000000",
        "state": "ST",
        "street": "Avenue",
    }


@pytest.fixture
def user_data(address_data):
    return {
        "id": "a72fcbe5-1103-4acc-a77b-954b46bc7ba8",
        "address": address_data,
        "email": "user1@email.com",
        "is_active": True,
        "name": "User Name",
        "password": "abc123",
        "permissions": ["create", "update", "delete"],
    }
