# app/middlewares/basic_auth.py
from __future__ import annotations

import base64
import secrets
from collections.abc import Awaitable, Callable
from urllib.parse import urlparse

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from app.settings import settings


# ------------------------------------------------------------
# 🔒 Shared Auth Logic
# ------------------------------------------------------------
def _verify_basic_credentials(username: str, password: str) -> bool:
    """Compare credentials safely against environment settings."""
    return secrets.compare_digest(
        username, settings.backoffice_username
    ) and secrets.compare_digest(password, settings.backoffice_password)


def _decode_basic_auth_header(auth_header: str | None) -> tuple[str, str]:
    """Decode a Basic Authorization header into (username, password)."""
    if auth_header is None or not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": 'Basic realm="Restricted Area"'},
        )

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username, password
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authorization header format",
        ) from None


# ------------------------------------------------------------
# 🧩 FastAPI Dependency (for Swagger + endpoints)
# ------------------------------------------------------------
basic_auth = HTTPBasic()


# B008: FastAPI pattern — Depends() is not executed immediately
async def secure_basic_auth(
    credentials: HTTPBasicCredentials = Depends(basic_auth),  # noqa: B008
) -> bool:
    """
    Dependency used in FastAPI routes to enforce Basic Auth and show lock in Swagger.
    """
    if not _verify_basic_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": 'Basic realm="Restricted Area"'},
        )
    return True


# ------------------------------------------------------------
# 🧱 Middleware (for automatic enforcement on restricted routes)
# ------------------------------------------------------------
class BasicAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware enforcing Basic Auth for restricted ports or paths.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.port_ip_restricted: list[int] = [
            settings.old_backoffice_port,
            settings.new_backoffice_port,
        ]
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=10.0)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Check for X-Original-URL header first (set by nginx proxy)
        original_url = request.headers.get("x-original-url")
        if original_url:
            parsed = urlparse(original_url)
            port = parsed.port or 0
        else:
            # Fallback to the current request URL port
            port = int(request.headers.get("x-forwarded-port", request.url.port or 0))

        # Skip if not in restricted context
        if port not in self.port_ip_restricted:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        try:
            username, password = _decode_basic_auth_header(auth_header)
        except HTTPException as exc:
            return Response(
                status_code=exc.status_code,
                content=exc.detail,
                headers=exc.headers or {},
            )

        if not _verify_basic_credentials(username, password):
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="Restricted Area"'},
            )

        return await call_next(request)
