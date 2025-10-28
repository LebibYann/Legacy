from __future__ import annotations

from fastapi import FastAPI

from app.api import base as base_api
from app.api import family as family_api
from app.api import individual as individual_api
from app.constants import PREFIX
from app.middlewares.basic_auth import BasicAuthMiddleware
from app.middlewares.fallback_proxy import ProxyWithFallbackMiddleware
from app.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        docs_url=f"{PREFIX}/docs",
        redoc_url=f"{PREFIX}/redoc",
        openapi_url=f"{PREFIX}/openapi.json",
    )

    # Middleware for fallback proxy
    app.add_middleware(ProxyWithFallbackMiddleware)

    # Middleware for Basic Auth
    app.add_middleware(BasicAuthMiddleware)

    # Routers
    app.include_router(base_api.router, prefix=PREFIX)
    app.include_router(family_api.router, prefix=PREFIX)
    app.include_router(individual_api.router, prefix=PREFIX)

    return app


app = create_app()
