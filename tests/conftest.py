import pytest
from alembic.config import main
from fastapi.testclient import TestClient
from jose import jwt

from sample_fast_api.config import settings
from sample_fast_api.main import db, get_app

settings.TEST_ENV = True


@pytest.fixture
def client():
    main(["--raiseerr", "upgrade", "head"])
    test_app = get_app(db, settings.TEST_DATABASE_URL)
    encoded_jwt = jwt.encode({"sub": "username"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with TestClient(test_app) as client:
        token = f"bearer {encoded_jwt}"
        client.headers.update({"Authorization": token})
        yield client

    main(["--raiseerr", "downgrade", "base"])
