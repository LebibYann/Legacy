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
    """
    Try modern target first (e.g. Vite/Svelte app), then fall back to legacy.
    Fallback triggers on network errors and on selected status codes (404/5xx by default).
    """

    # Status codes that should trigger a fallback attempt on the next target
    FALLBACK_STATUSES: set[int] = {
        404, 405, 409, 422,              # "feature not implemented" / route missing
        500, 501, 502, 503, 504, 521, 522, 523, 524  # server/network failures
    }

    def __init__(self, app):
        super().__init__(app)
        # Map external entry port -> primary modern target port
        # 2316 -> (try 5173 on backoffice-dev, then fallback to legacy-geneweb:2316)
        # 2317 -> (try 5174 on backoffice-dev (if you want), else fallback to legacy-geneweb:2317)
        self.ports: dict[int, int] = {
            settings.old_backoffice_port: settings.new_backoffice_port,
            settings.old_frontend_port: settings.new_frontend_port,
        }

        self.dns_for_ports: dict[int, str] = {
            settings.old_backoffice_port: settings.legacy_dns,
            settings.old_frontend_port: settings.frontend_dns,
            settings.new_backoffice_port: settings.backoffice_dns,
            settings.new_frontend_port: settings.frontend_dns,
        }
        # Single async client reused (keep-alive)
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=10.0)

    async def dispatch(self, request: Request, call_next):
        port: int = request.url.port or 0
        path_qs = request.url.path
        if request.url.query:
            path_qs += f"?{request.url.query}"

        if port in self.ports and not request.url.path.startswith((PREFIX)):
            # 👇 Respecte ton ordre: d'abord moderne, puis legacy
            # (modern_port, modern_dns) puis (legacy_port=entry port, legacy dns)
            targets: list[tuple[int, str]] = [
                (self.ports[port], self.dns_for_ports[self.ports[port]]),
                (port, self.dns_for_ports[port]),
            ]

            # Corps lu une seule fois (sinon il est consommé)
            body = await request.body()
            # Copie de headers, on laisse httpx recalculer content-length/connection
            base_headers = dict(request.headers)
            for h in ("content-length", "connection", "host", "accept-encoding"):
                base_headers.pop(h, None)

            for tgt_port, tgt_dns in targets:
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

                    # Si la réponse est "bonne" (pas dans la liste fallback), on la renvoie telle quelle
                    if status not in self.FALLBACK_STATUSES:
                        # Filtrage des hop-by-hop headers
                        headers = dict(resp.headers)
                        for bad in ("content-encoding", "transfer-encoding", "connection", "content-length"):
                            headers.pop(bad, None)

                        # Préserver plusieurs Set-Cookie si présents
                        set_cookies: Iterable[str] = resp.headers.get_list("set-cookie")
                        # On reconstruit une Response pour ne pas perdre les Set-Cookie multiples
                        out = Response(content=await resp.aread(), status_code=status, headers=headers)
                        for sc in set_cookies:
                            out.headers.add("set-cookie", sc)
                        return out

                    # Sinon on tente le fallback (prochaine cible)
                    log.info("[proxy] falling back from %s (status %s)", url, status)

                except Exception as e:
                    # Erreur réseau/timeouts → fallback sur la cible suivante
                    log.warning("[proxy] %s failed (%s), trying next target…", url, e)
                    continue

            # Toutes les cibles ont échoué → on laisse FastAPI gérer
            log.info("[proxy] all targets failed for %s, forwarding to app", request.url)

        # Pas de port concerné ou aucun target n'a répondu correctement → FastAPI continue
        return await call_next(request)
