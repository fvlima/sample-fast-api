import binascii
import hashlib
import os
import typing
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Address(BaseModel):
    id: UUID = ""
    city: str = Field(..., min_length=4, max_length=32, description="The user's address city")
    complement: str = Field("", max_length=128, description="The user's address complement")
    country: str = Field(..., max_length=64, description="The user's address country")
    number: str = Field(..., max_length=16, description="The user's address number")
    postal_code: str = Field(..., max_length=8, description="The user's address postal code")
    state: str = Field(..., min_length=2, max_length=2, description="The user's address state")
    street: str = Field(..., max_length=128, description="The user's address street")

    class Config:
        orm_mode = True

    def __str__(self):
        return f"{self.street}, {self.number}, {self.postal_code}, {self.country}, {self.state}"


class User(BaseModel):
    id: UUID = ""
    address: Address = None
    email: EmailStr
    is_active: bool
    name: str = Field(..., min_length=8, max_length=64, description="The name that represents the user")
    permissions: typing.List[str] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "a2a18886-d3a2-4774-8e5f-69f7e1057a7d",
                "address": {},
                "name": "John Doe",
                "email": "user@email.com",
                "is_active": True,
                "password": "f1edef6a67e7445c8c88d189fd7ff63b",
                "permissions": ["create", "update", "delete"],
            }
        }

    def __str__(self):
        return f"{self.id}, {self.name}, {self.email}"


class UserCreate(User):
    password: str = Field(
        None, min_length=6, max_length=16, description="A text value with length between 6 and 16 characters"
    )

    def hash_password(self):
        if not self.password or len(self.password) > 16:
            return

        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode()
        pwd_hash = hashlib.pbkdf2_hmac("sha512", self.password.encode(), salt, 100000)
        pwd_hex = binascii.hexlify(pwd_hash)

        return salt.decode() + pwd_hex.decode()
