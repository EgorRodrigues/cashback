from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.db import engine
from src.orm import start_mappers

from .routers import auth, purchases, resellers


def create_app():
    app = FastAPI()

    app.include_router(resellers.router)
    app.include_router(purchases.router)
    app.include_router(auth.router)

    @app.on_event("startup")
    async def startup():
        start_mappers()

    @app.on_event("shutdown")
    async def shutdown():
        await engine.dispose()
        clear_mappers()

    return app
