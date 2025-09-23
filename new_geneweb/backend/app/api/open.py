from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["open"])


@router.get("/health", summary="Healthcheck")
def health() -> dict[str, str]:
    return {"status": "ok"}
