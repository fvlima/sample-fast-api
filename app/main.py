import databases
from fastapi import FastAPI, Request

from .config import settings
from app.apps.users import routers

app = FastAPI()
app.include_router(routers.router)

db = databases.Database(settings.DATABASE_URL)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = db
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
