from __future__ import annotations

from fastapi import APIRouter, Depends, Path

from app.persistence.DBConnector import DBConnector
from app.schemas.individual import (
    IndividualCreateRequest,
    IndividualCreateResponse,
    IndividualDeleteResponse,
    IndividualGetResponse,
)
from app.services.individual_service import IndividualService
from app.shared_instances import get_db_connector

router = APIRouter(prefix="/bases/{base_id}/individuals", tags=["Individual"])

# ---- POST Requests ----


@router.post(
    "",
    summary="Create an individual",
    description="Create a new individual in the specified base.",
    response_model=IndividualCreateResponse,
    status_code=201,
)
async def create_individual(
    individual: IndividualCreateRequest,
    base_id: int = Path(..., description="Target base ID"),
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> IndividualCreateResponse:
    service = IndividualService(db)
    return await service.create(base_id=base_id, payload=individual)


# ---- GET Requests ----


@router.get(
    "/{individual_id}",
    summary="Get an individual",
    description="Retrieve an individual's details by ID in the specified base.",
    response_model=IndividualGetResponse,
)
async def get_individual(
    base_id: int = Path(..., description="Target base ID"),
    individual_id: int = Path(..., description="Individual ID to retrieve"),
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> IndividualGetResponse:
    service = IndividualService(db)
    return await service.get(base_id=base_id, individual_id=individual_id)


# ---- DELETE Requests ----


@router.delete(
    "/{individual_id}",
    summary="Delete an individual",
    description="Delete an individual by ID in the specified base.",
    response_model=IndividualDeleteResponse,
)
async def delete_individual(
    base_id: int = Path(..., description="Target base ID"),
    individual_id: int = Path(..., description="Individual ID to delete"),
    db: DBConnector = Depends(get_db_connector),  # noqa: B008
) -> IndividualDeleteResponse:
    service = IndividualService(db)
    return await service.delete(base_id=base_id, individual_id=individual_id)
