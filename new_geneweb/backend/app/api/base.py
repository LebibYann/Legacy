from __future__ import annotations

from fastapi import APIRouter

from app.schemas.base import (
    BaseCreateRequest,
    BaseCreateResponse,
    BaseListResponse,
)
from app.services.base_service import BaseService

router = APIRouter(prefix="/bases", tags=["Base"])


# ---- POST Requests ----
@router.post(
    "",
    summary="Create a new base",
    description="""
Create a new genealogical base in the system.

- **name**: The name of the base to be created.
""",
    response_model=BaseCreateResponse,
    status_code=201,
)
async def create_base(base: BaseCreateRequest) -> BaseCreateResponse:
    """
    Create a new base and return its details.
    """
    service = BaseService()
    return await service.create(payload=base)


# ---- GET Requests ----
@router.get(
    "",
    summary="List all bases",
    description="Retrieve the list of all available bases.",
    response_model=BaseListResponse,
)
async def list_bases() -> BaseListResponse:
    """
    Retrieve all existing bases in the system.
    """
    service = BaseService()
    return await service.list()
