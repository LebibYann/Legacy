from __future__ import annotations

from fastapi import APIRouter, Depends

from app.middlewares.basic_auth import secure_basic_auth
from app.persistence.DBConnector import DBConnector
from app.schemas.base import (
    BaseCreateRequest,
    BaseCreateResponse,
    BaseDeleteResponse,
    BaseListResponse,
)
from app.services.base_service import BaseService
from app.shared_instances import get_db_connector

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
    dependencies=[Depends(secure_basic_auth)],
)
async def create_base(
    base: BaseCreateRequest,
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> BaseCreateResponse:
    """
    Create a new base and return its details.
    """
    service = BaseService(db)
    return await service.create(payload=base)


# ---- GET Requests ----
@router.get(
    "",
    summary="List all bases",
    description="Retrieve the list of all available bases.",
    response_model=BaseListResponse,
)
async def list_bases(
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> BaseListResponse:
    """
    Retrieve all existing bases in the system.
    """
    return await BaseService(db).list()


# ---- DELETE Requests ----
@router.delete(
    "/{base_name}",
    summary="Delete a base",
    description="""
Delete an existing genealogical base from the system.

- **base_name**: The name of the base to delete.
""",
    response_model=BaseDeleteResponse,
    dependencies=[Depends(secure_basic_auth)],
)
async def delete_base(
    base_name: str,
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> BaseDeleteResponse:
    """
    Delete a base and return operation status.
    """
    service = BaseService(db)
    return await service.delete(base_name=base_name)
