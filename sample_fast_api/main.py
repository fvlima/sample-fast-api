from fastapi import FastAPI
from gino.ext.starlette import Gino

from .config import settings
from .routers import load_routers

db = Gino()


def get_app(db, database_url):
    app = FastAPI()
    db.config["dsn"] = database_url
    db.init_app(app)
    load_routers(app)
    return app


app = get_app(db, settings.DATABASE_URL)
