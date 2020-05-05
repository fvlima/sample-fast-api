from sample_fast_api.apps.users.models import Address, User


class BaseFactory:
    @classmethod
    async def create(cls, **kwargs):
        data = {}

        for k, v in cls.__dict__.items():
            if k in ("__doc__", "__module__", "Meta"):
                continue

            if k in kwargs:
                data[k] = kwargs.get(k)
            else:
                if isinstance(v, type):
                    obj = await v.create()
                    data[f"{k}_id"] = obj.id
                else:
                    data[k] = v

        model = cls.Meta.model
        return await model.create(**data)


class AddressFactory(BaseFactory):
    class Meta:
        model = Address

    city = "City"
    country = "Country"
    complement = ""
    number = "9999"
    postal_code = "00000000"
    state = "ST"
    street = "Avenue"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    address = AddressFactory
    name = "User Name"
    email = "user1@email.com"
    password = "abc123"
    is_active = True
    permissions = ["create", "update", "delete"]
