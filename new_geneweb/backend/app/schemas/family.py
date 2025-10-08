from __future__ import annotations

from pydantic import BaseModel, Field

# ============================================================
#  Base schema (shared by all requests & responses)
# ============================================================


class FamilyBase(BaseModel):
    father_id: int | None = Field(None, description="ID of the father, if known")
    mother_id: int | None = Field(None, description="ID of the mother, if known")
    same_sex_couple: bool = Field(
        False, description="True if both parents are of the same sex"
    )

    children_ids: list[int] = Field(
        default_factory=list, description="List of children IDs"
    )
    events_ids: list[int] = Field(
        default_factory=list, description="Associated genealogical event IDs"
    )

    source_family: str | None = Field(None, description="Source of this family data")
    source_individuals: str | None = Field(
        None, description="Source of the individual data"
    )
    comment: str | None = Field(None, description="Free-text comment about this family")


# ============================================================
#  Requests (inputs)
# ============================================================


class FamilyCreateRequest(FamilyBase):
    """Request schema for creating a family."""

    pass


class FamilyCreateToIndividualRequest(FamilyBase):
    """Request schema for creating a family linked to a specific individual."""

    individual_id: int = Field(
        ..., description="ID of the individual to link the new family to"
    )


class FamilyUpdateRequest(FamilyBase):
    """Request schema for updating an existing family."""

    pass


class FamilyMergeRequest(BaseModel):
    """Request schema for merging two families."""

    source_family_id: int = Field(..., description="ID of the source family")
    target_family_id: int = Field(..., description="ID of the target family")


class FamilyGetRequest(BaseModel):
    """Request schema for retrieving a family."""

    family_id: int = Field(..., description="ID of the family to retrieve")


class FamilyDeleteRequest(BaseModel):
    """Request schema for deleting a family."""

    pass


# ============================================================
#  Responses (outputs)
# ============================================================


class FamilyCreateResponse(BaseModel):
    """Response schema after creating a family."""

    family_id: int = Field(..., description="Newly created family ID")


class FamilyCreateToIndividualResponse(BaseModel):
    """Response schema after creating a family linked to an individual."""

    family_id: int = Field(..., description="Newly created family ID")
    individual_id: int = Field(..., description="ID of the linked individual")


class FamilyUpdateResponse(BaseModel):
    """Response schema after updating a family."""

    family_id: int = Field(..., description="Updated family ID")


class FamilyMergeResponse(BaseModel):
    """Response schema after merging two families."""

    family_id: int = Field(..., description="Resulting merged family ID")


class FamilyGetResponse(FamilyBase):
    """Response schema for retrieving a family."""

    family_id: int = Field(..., description="ID of the retrieved family")


class FamilyDeleteResponse(BaseModel):
    """Response schema after deleting a family."""

    success: bool = Field(
        True, description="Indicates if the family was successfully deleted"
    )
    # Excluded so the API returns only {"success": true} as expected by tests
    message: str | None = Field(
        None, description="Optional message about the operation result", exclude=True
    )
