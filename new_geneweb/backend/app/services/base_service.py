from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.base import (
    Base,
    BaseCreateRequest,
    BaseCreateResponse,
    BaseDeleteResponse,
    BaseListResponse,
)


class BaseService:
    """
    Service layer responsible for managing genealogical bases.
    Handles logic for creating, listing, and deleting bases.
    """

    def __init__(self, session: AsyncSession | None = None) -> None:
        # Keep session reference for DB access (future)
        self.session = session

    # ---- Create ----
    async def create(self, payload: BaseCreateRequest) -> BaseCreateResponse:
        """
        Create a new genealogical base.
        """
        # TODO: Insert into database
        return BaseCreateResponse(base_id=1, name=payload.name)

    # ---- List ----
    async def list(self) -> BaseListResponse:
        """
        Retrieve all existing bases.
        """
        # TODO: Replace with DB fetch
        return BaseListResponse(bases=[Base(name="Default Base")])

    # ---- Delete ----
    async def delete(self, base_id: int) -> BaseDeleteResponse:
        """
        Delete a base by its ID.
        """
        # TODO: Add DB deletion logic
        return BaseDeleteResponse(success=True, message=None)
