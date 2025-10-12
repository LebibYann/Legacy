from __future__ import annotations

from fastapi import FastAPI

from app.api import open as open_api
from app.api import restricted as restricted_api
from app.settings import settings
from app.middlewares.ip_filter import IpAllowlistMiddleware
from app.middlewares.fallback_proxy import ProxyWithFallbackMiddleware

from app.constants import PREFIX


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name,
                  docs_url=f"{PREFIX}/docs",
                  redoc_url=f"{PREFIX}/redoc",
                  openapi_url=f"{PREFIX}/openapi.json",)


    # Middleware for IP allowlist
    app.add_middleware(IpAllowlistMiddleware, allowed_ips=settings.allowed_ips)

    # Middleware for fallback proxy
    app.add_middleware(ProxyWithFallbackMiddleware)

    # Routers
    app.include_router(open_api.router, prefix=PREFIX)
    app.include_router(restricted_api.router, prefix=PREFIX)

    return app


app = create_app()
