from __future__ import annotations

from pydantic import BaseModel, Field

# ============================================================
#  Base schema (shared structure)
# ============================================================


class Base(BaseModel):
    """Represents a genealogical base in the system."""

    name: str = Field(..., description="Name of the genealogical base")


# ============================================================
#  Requests
# ============================================================


class BaseCreateRequest(Base):
    """Request body for creating a new base."""

    pass


class BaseListRequest(BaseModel):
    """Placeholder request for listing bases (currently unused)."""

    pass


class BaseDeleteRequest(BaseModel):
    """Request body for deleting a base."""

    base_id: int = Field(..., description="ID of the base to delete")


# ============================================================
#  Responses
# ============================================================


class BaseCreateResponse(Base):
    """Response after creating a base."""

    base_id: int = Field(..., description="ID of the newly created base")
    pass


class BaseListResponse(BaseModel):
    """Response containing a list of all existing bases."""

    bases: list[Base] = Field(..., description="List of available bases")


class BaseDeleteResponse(BaseModel):
    """Response after deleting a base."""

    success: bool = Field(
        True, description="Indicates if the base was successfully deleted"
    )
    message: str | None = Field(
        None, description="Optional message about the operation result"
    )
