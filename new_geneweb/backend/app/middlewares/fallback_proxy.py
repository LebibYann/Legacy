# app/middlewares/proxy_with_fallback.py
from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Iterable
from urllib.parse import urlparse

import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.constants import PREFIX
from app.settings import settings

log = logging.getLogger(__name__)


class ProxyWithFallbackMiddleware(BaseHTTPMiddleware):
    FALLBACK_STATUSES: set[int] = {
        403,
        404,
        405,
        409,
        422,
        500,
        501,
        502,
        503,
        504,
        521,
        522,
        523,
        524,
    }

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.ports: dict[int, int] = {
            settings.old_backoffice_port: settings.new_backoffice_port,
            settings.old_frontend_port: settings.new_frontend_port,
        }
        self.dns_for_ports: dict[int, str] = {
            settings.old_backoffice_port: settings.legacy_dns,
            settings.old_frontend_port: settings.legacy_dns,
            settings.new_backoffice_port: settings.backoffice_dns,
            settings.new_frontend_port: settings.legacy_dns,
            # TODO Replace:
            # settings.new_frontend_port: settings.legacy_dns
            # with
            # settings.new_frontend_port: settings.frontend_dns
            # when frontend is properly implemented
        }

        self.client = httpx.AsyncClient(follow_redirects=True, timeout=10.0)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Check for X-Original-URL header first (set by nginx proxy)
        original_url = request.headers.get("x-original-url")
        if original_url:
            # Parse the original URL to get the port and path
            parsed = urlparse(original_url)
            port = parsed.port or 0
            path_qs = parsed.path
            if parsed.query:
                path_qs += f"?{parsed.query}"
        else:
            # Fallback to the current request URL
            port = int(request.headers.get("x-forwarded-port", request.url.port or 0))
            path_qs = request.url.path
            if request.url.query:
                path_qs += f"?{request.url.query}"

        # The proxy is only applied if the port is in the mapping,
        # and the route is not /api (PREFIX)
        if port in self.ports and not request.url.path.startswith(PREFIX):
            body = await request.body()
            base_headers = dict(request.headers)
            for h in ("content-length", "connection", "host", "accept-encoding"):
                base_headers.pop(h, None)

            for tgt_port, tgt_dns in [
                (self.ports[port], self.dns_for_ports[self.ports[port]]),
                (port, self.dns_for_ports[port]),
            ]:
                url = f"http://{tgt_dns}:{tgt_port}{path_qs}"
                try:
                    return await self.attempt_proxy(url, request, base_headers, body)
                except Exception as e:
                    log.warning("[proxy] %s failed (%s), trying next target…", url, e)

        return await call_next(request)

    async def attempt_proxy(
        self,
        url: str,
        request: Request,
        base_headers: dict[str, str],
        body: bytes | None,
    ) -> Response:

        proxied = self.client.build_request(
            method=request.method,
            url=url,
            headers=base_headers,
            content=body if body else None,
        )
        resp = await self.client.send(proxied)
        status = resp.status_code
        log.info(
            "[proxy] %s %s → %s [%s]",
            request.method,
            request.url,
            url,
            status,
        )

        if status not in self.FALLBACK_STATUSES:
            # Read the entire body
            content_bytes = await resp.aread()
            # Decoding possible depending on encoding
            # assume utf-8 (or adjust)
            text = None
            try:
                text = content_bytes.decode("utf-8")
            except Exception as e:
                # unable to decode, leave as-is
                log.warning("[proxy] %s failed to decode response body (%s)", url, e)

            if text is not None and "text/html" in resp.headers.get("content-type", ""):
                replaced = text.replace(settings.legacy_dns, request.url.hostname or "")
                content_bytes = replaced.encode("utf-8")

            headers = dict(resp.headers)
            for bad in (
                "content-encoding",
                "transfer-encoding",
                "connection",
                "content-length",
            ):
                headers.pop(bad, None)

            set_cookies: Iterable[str] = resp.headers.get_list("set-cookie")
            out = Response(content=content_bytes, status_code=status, headers=headers)
            for sc in set_cookies:
                out.headers["set-cookie"] = sc
            return out

        log.info("[proxy] falling back from %s (status %s)", url, status)
        raise Exception(f"Proxying failed error: {status}")
