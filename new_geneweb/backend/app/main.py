from __future__ import annotations

from fastapi import FastAPI

from app.api import open as open_api
from app.api import restricted as restricted_api
from app.settings import settings
from app.utils.ip_filter import IpAllowlistMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    # Middleware for IP allowlist
    app.add_middleware(IpAllowlistMiddleware, allowed_ips=settings.allowed_ips)

    # Routers
    app.include_router(open_api.router)
    app.include_router(restricted_api.router)

    return app


app = create_app()
