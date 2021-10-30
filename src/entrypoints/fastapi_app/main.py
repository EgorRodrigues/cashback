from fastapi import FastAPI

from src.db import database
from src.orm import start_mappers

from .routers import auth, purchases, resellers


def create_app():
    app = FastAPI()

    app.include_router(resellers.router)
    app.include_router(purchases.router)
    app.include_router(auth.router)

    @app.on_event("startup")
    async def startup():
        await database.connect()
        start_mappers()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app
