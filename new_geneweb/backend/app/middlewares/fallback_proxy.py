# app/middlewares/proxy_with_fallback.py
from __future__ import annotations

import logging
from typing import Iterable

import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.constants import PREFIX
from app.settings import settings

log = logging.getLogger(__name__)

class ProxyWithFallbackMiddleware(BaseHTTPMiddleware):
    FALLBACK_STATUSES: set[int] = {
        403, 404, 405, 409, 422,
        500, 501, 502, 503, 504, 521, 522, 523, 524
    }

    def __init__(self, app):
        super().__init__(app)
        self.ports: dict[int, int] = {
            settings.old_backoffice_port: settings.new_backoffice_port,
            settings.old_frontend_port: settings.new_frontend_port,
        }
        self.dns_for_ports: dict[int, str] = {
            settings.old_backoffice_port: settings.legacy_dns,
            settings.old_frontend_port: settings.legacy_dns,
            settings.new_backoffice_port: settings.backoffice_dns,
            settings.new_frontend_port: settings.frontend_dns,
        }
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=10.0)

    async def dispatch(self, request: Request, call_next):
        port: int = request.url.port or 0
        path_qs = request.url.path
        if request.url.query:
            path_qs += f"?{request.url.query}"

        # On n'applique le proxy que si le port est dans la mappage, et la route n’est pas /api (PREFIX)
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
                    proxied = self.client.build_request(
                        method=request.method,
                        url=url,
                        headers=base_headers,
                        content=body if body else None,
                    )
                    resp = await self.client.send(proxied)
                    status = resp.status_code
                    log.info("[proxy] %s %s → %s [%s]", request.method, request.url, url, status)

                    if status not in self.FALLBACK_STATUSES:
                        # On lit tout le corps
                        content_bytes = await resp.aread()
                        # Décodage possible selon encodage — on suppose utf-8 (ou ajuster)
                        text = None
                        try:
                            text = content_bytes.decode("utf-8")
                        except Exception:
                            # impossible de décoder, on laisse tel quel
                            pass

                        if text is not None and "text/html" in resp.headers.get("content-type", ""):
                            # Remplacement voulu
                            print(request.url.hostname)
                            replaced = text.replace("legacy-geneweb", f"{request.url.hostname}")  # ou autre URL
                            content_bytes = replaced.encode("utf-8")

                        headers = dict(resp.headers)
                        for bad in ("content-encoding", "transfer-encoding", "connection", "content-length"):
                            headers.pop(bad, None)

                        set_cookies: Iterable[str] = resp.headers.get_list("set-cookie")
                        out = Response(content=content_bytes, status_code=status, headers=headers)
                        for sc in set_cookies:
                            out.headers.add("set-cookie", sc)
                        return out

                    log.info("[proxy] falling back from %s (status %s)", url, status)
                except Exception as e:
                    log.warning("[proxy] %s failed (%s), trying next target…", url, e)
                    continue

        return await call_next(request)
