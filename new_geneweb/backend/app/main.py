from __future__ import annotations

from fastapi import FastAPI

from app.api import base as base_api
from app.api import family as family_api
from app.api import individual as individual_api
from app.settings import settings
from app.utils.ip_filter import IpAllowlistMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    # Middleware for IP allowlist
    app.add_middleware(IpAllowlistMiddleware, allowed_ips=settings.allowed_ips)

    # Routers
    app.include_router(base_api.router)
    app.include_router(family_api.router)
    app.include_router(individual_api.router)

    return app


app = create_app()
