from __future__ import annotations

from app.persistence.DBConnector import DBConnector
from app.schemas.individual import (
    GenderType,
    IndividualCreateRequest,
    IndividualCreateResponse,
    IndividualDeleteResponse,
    IndividualGetResponse,
)

from .a_service import AService


class IndividualService(AService):
    """
    Service layer for individual-related operations.
    Handles the domain logic, leaving persistence to repository layer (future).
    """

    def __init__(self, session: DBConnector) -> None:
        # Future-proof: keep session for DB access
        super().__init__(session)

    # ---- Create ----
    async def create(
        self, base_id: int, payload: IndividualCreateRequest
    ) -> IndividualCreateResponse:
        """
        Create a new individual in the given base.
        """
        # TODO: add database logic
        return IndividualCreateResponse(individual_id=1)

    # ---- Get ----
    async def get(self, base_id: int, individual_id: int) -> IndividualGetResponse:
        """
        Retrieve an individual's details by ID.
        """
        # TODO: add database logic
        return IndividualGetResponse(
            individual_id=individual_id,
            first_name="John",
            last_name="Doe",
            public_name=None,
            image_url=None,
            nickname=None,
            alias=None,
            alias_first_name=None,
            alias_last_name=None,
            profession=None,
            source=None,
            number=None,
            gender=GenderType.UNKNOWN,
            access_type_id=None,
            insert_nickname=False,
            insert_alias=False,
            insert_firstname_alias=False,
            insert_lastname_alias=False,
            birth_place=None,
            birth_date1=None,
            birth_date_range=None,
            birth_date2=None,
            birth_date3=None,
            birth_notes=None,
            birth_source=None,
            birth_witnesses_ids=[],
            baptism_place=None,
            baptism_date1=None,
            baptism_date_range=None,
            baptism_date2=None,
            baptism_date3=None,
            baptism_notes=None,
            baptism_source=None,
            baptism_witnesses_ids=[],
            death_place=None,
            death_date1=None,
            death_date_range=None,
            death_date2=None,
            death_date3=None,
            death_notes=None,
            death_source=None,
            death_witnesses_ids=[],
            burial_place=None,
            burial_date1=None,
            burial_date_range=None,
            burial_date2=None,
            burial_date3=None,
            burial_notes=None,
            burial_source=None,
            burial_witnesses_ids=[],
            events_ids=[],
            relations_ids=[],
            title_ids=[],
            notes=None,
        )

    # ---- Delete ----
    async def delete(
        self, base_id: int, individual_id: int
    ) -> IndividualDeleteResponse:
        """
        Delete an individual by ID.
        """
        # TODO: add database logic
        return IndividualDeleteResponse(
            success=True, message="Individual deleted successfully"
        )
