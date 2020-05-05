import uuid

import pytest
from alembic.config import main
from fastapi.testclient import TestClient

from sample_fast_api.config import settings
from sample_fast_api.main import db, get_app

settings.TEST_ENV = True


@pytest.fixture
def client():
    main(["--raiseerr", "upgrade", "head"])

    test_app = get_app(db, settings.TEST_DATABASE_URL)
    with TestClient(test_app) as client:
        token = f"Token {uuid.uuid4()}"
        client.headers.update({"Authorization": token})
        yield client

    main(["--raiseerr", "downgrade", "base"])
