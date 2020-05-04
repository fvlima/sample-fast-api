from sqlalchemy import create_engine

from .config import settings

engine = create_engine(settings.DATABASE_URL)


def create_databases():
    from app.apps.users.tables import metadata

    metadata.create_all(bind=engine)
