from __future__ import annotations

from fastapi import APIRouter, Path

from app.schemas.family import (
    FamilyCreateRequest,
    FamilyCreateResponse,
    FamilyCreateToIndividualRequest,
    FamilyCreateToIndividualResponse,
    FamilyDeleteResponse,
    FamilyGetResponse,
    FamilyMergeRequest,
    FamilyMergeResponse,
    FamilyUpdateRequest,
    FamilyUpdateResponse,
)
from app.services.family_service import FamilyService

router = APIRouter(prefix="/bases/{base_id}/families", tags=["Family"])

# ---- POST Requests ----


@router.post(
    "",
    summary="Create a family",
    description="Create a new family in the specified base.",
    response_model=FamilyCreateResponse,
    status_code=201,
)
async def create_family(
    family: FamilyCreateRequest,
    base_id: int = Path(..., description="Target base ID"),
) -> FamilyCreateResponse:
    service = FamilyService()
    return await service.create(base_id=base_id, payload=family)


@router.post(
    "/to",
    summary="Create a family related to an individual",
    description="Create a new family and associate it with an existing individual.",
    response_model=FamilyCreateToIndividualResponse,
    status_code=201,
)
async def create_family_to_individual(
    family: FamilyCreateToIndividualRequest,
    base_id: int = Path(..., description="Target base ID"),
) -> FamilyCreateToIndividualResponse:
    service = FamilyService()
    return await service.create_to_individual(base_id=base_id, payload=family)


# ---- PUT Requests ----


@router.put(
    "/{family_id}",
    summary="Update a family",
    description="Update a family's information in the specified base.",
    response_model=FamilyUpdateResponse,
)
async def update_family(
    family: FamilyUpdateRequest,
    base_id: int = Path(..., description="Target base ID"),
    family_id: int = Path(..., description="Family ID to update"),
) -> FamilyUpdateResponse:
    service = FamilyService()
    return await service.update(base_id=base_id, family_id=family_id, payload=family)


# ---- PATCH Requests ----


@router.patch(
    "/merge",
    summary="Merge two families",
    description="Merge two existing families in the same base.",
    response_model=FamilyMergeResponse,
)
async def merge_families(
    payload: FamilyMergeRequest,
    base_id: int = Path(..., description="Target base ID"),
) -> FamilyMergeResponse:
    service = FamilyService()
    return await service.merge(base_id=base_id, payload=payload)


# ---- GET Requests ----


@router.get(
    "/{family_id}",
    summary="Get family details",
    description="Retrieve detailed information about a specific family.",
    response_model=FamilyGetResponse,
)
async def get_family(
    base_id: int = Path(..., description="Target base ID"),
    family_id: int = Path(..., description="Family ID to retrieve"),
) -> FamilyGetResponse:
    service = FamilyService()
    return await service.get(base_id=base_id, family_id=family_id)


# ---- DELETE Requests ----


@router.delete(
    "/{family_id}",
    summary="Delete a family",
    description="Remove a family from the specified base.",
)
async def delete_family(
    base_id: int = Path(..., description="Target base ID"),
    family_id: int = Path(..., description="Family ID to delete"),
) -> FamilyDeleteResponse:
    service = FamilyService()
    return await service.delete(base_id=base_id, family_id=family_id)
