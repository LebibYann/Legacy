from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


class IpAllowlistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, allowed_ips: Iterable[str]) -> None:
        super().__init__(app)
        self.allowed: set[str] = set(allowed_ips)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        client_ip = request.client.host if request.client else ""
        if request.url.path.startswith("/restricted") and client_ip not in self.allowed:
            raise HTTPException(status_code=403, detail="IP not allowed")
        return await call_next(request)
