from __future__ import annotations

from app.persistence.DBConnector import DBConnector
from app.schemas.base import (
    Base,
    BaseCreateRequest,
    BaseCreateResponse,
    BaseDeleteResponse,
    BaseListResponse,
)
from app.settings import settings

from .a_service import AService


class BaseService(AService):
    """
    Service layer responsible for managing genealogical bases.
    Handles logic for creating, listing, and deleting bases.
    """

    def __init__(self, session: DBConnector) -> None:
        # Keep session reference for DB access (future)
        super().__init__(session)

    # ---- Create ----
    async def create(self, payload: BaseCreateRequest) -> BaseCreateResponse:
        """
        Create a new genealogical base.
        """
        await self.session.create_geneweb_database(payload.name)
        return BaseCreateResponse(base_id=1, name=payload.name)

    # ---- List ----
    async def list(self) -> BaseListResponse:
        """
        Retrieve all existing bases.
        """
        bases: list[str] = self.session.list_geneweb_databases()
        return BaseListResponse(
            bases=[Base(name=base_name) for base_name in bases],
            port=settings.old_frontend_port,
        )

    # ---- Delete ----
    async def delete(self, base_name: str) -> BaseDeleteResponse:
        """
        Delete a base by its name.
        """
        await self.session.delete_geneweb_database(base_name)
        return BaseDeleteResponse(
            success=True, message=f"Base '{base_name}' successfully deleted"
        )
