from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/restricted", tags=["restricted"])


@router.get("/ping", summary="Restricted ping")
def ping() -> dict[str, str]:
    return {"pong": "restricted"}
