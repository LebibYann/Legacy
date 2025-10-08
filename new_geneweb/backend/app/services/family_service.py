from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

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


class FamilyService:
    """
    Service layer for family-related operations.
    Handles the domain logic, leaving persistence to repository layer (future).
    """

    def __init__(self, session: AsyncSession | None = None) -> None:
        # Future-proof: keep session for DB access
        self.session = session

    # ---- Create ----
    async def create(
        self, base_id: int, payload: FamilyCreateRequest
    ) -> FamilyCreateResponse:
        """
        Create a new family in the given base.
        """
        # TODO: add database logic
        return FamilyCreateResponse(family_id=1)

    # ---- Create (to individual) ----
    async def create_to_individual(
        self, base_id: int, payload: FamilyCreateToIndividualRequest
    ) -> FamilyCreateToIndividualResponse:
        """
        Create a new family linked to an existing individual.
        """
        # TODO: add database logic
        return FamilyCreateToIndividualResponse(
            family_id=1, individual_id=payload.individual_id
        )

    # ---- Update ----
    async def update(
        self, base_id: int, family_id: int, payload: FamilyUpdateRequest
    ) -> FamilyUpdateResponse:
        """
        Update an existing family in a given base.
        """
        # TODO: add database logic
        return FamilyUpdateResponse(family_id=family_id)

    # ---- Merge ----
    async def merge(
        self, base_id: int, payload: FamilyMergeRequest
    ) -> FamilyMergeResponse:
        """
        Merge two families in the same base.
        """
        # TODO: add database logic
        return FamilyMergeResponse(family_id=payload.target_family_id)

    # ---- Get ----
    async def get(self, base_id: int, family_id: int) -> FamilyGetResponse:
        """
        Retrieve details of a specific family.
        """
        # TODO: add database logic
        return FamilyGetResponse(
            family_id=family_id,
            father_id=None,
            mother_id=None,
            same_sex_couple=False,
            children_ids=[],
            events_ids=[],
            source_family=None,
            source_individuals=None,
            comment=None,
        )

    # ---- Delete ----
    async def delete(self, base_id: int, family_id: int) -> FamilyDeleteResponse:
        """
        Delete a family by its ID.
        """
        # TODO: add database logic
        return FamilyDeleteResponse(success=True, message=None)
