from fastapi import FastAPI
from features.users.controller import router as users_router


def register_routers(app: FastAPI):
    """
    Register all routers with the FastAPI application.
    This function should be called after creating the FastAPI app instance.
    """
    app.include_router(users_router)