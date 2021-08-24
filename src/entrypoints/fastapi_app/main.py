from fastapi import FastAPI

from src.config import database

from .routers import auth, purchases, resellers


def create_app():
    app = FastAPI()

    app.include_router(resellers.router)
    app.include_router(purchases.router)
    app.include_router(auth.router)

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app
