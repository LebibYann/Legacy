from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

# ============================================================
# Enumerations
# ============================================================


class RelationType(str, Enum):
    """Defines the type of parental relationship."""

    ADOPTIVE_PARENTS = "adoptive_parents"
    BIOLOGICAL_PARENTS = "biological_parents"
    FOSTER_PARENTS = "foster_parents"


class GenderType(str, Enum):
    """Defines the gender of an individual."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


# ============================================================
# Base schema (shared by all requests & responses)
# ============================================================


class TitleBase(BaseModel):
    """Represents a noble or professional title associated with an individual."""

    title: str | None = Field(None, description="Full title (e.g. 'Duke', 'Doctor')")
    name: str | None = Field(None, description="Title name or associated domain")
    fief: str | None = Field(None, description="Fief or territory name, if applicable")
    rank: str | None = Field(None, description="Title rank (e.g. 'Count', 'Baron')")
    main_title: bool = Field(False, description="True if this is the primary title")

    begin_date: str | None = Field(
        None, description="Start date of title validity (ISO format)"
    )
    end_date: str | None = Field(
        None, description="End date of title validity (ISO format)"
    )
    begin_date_alt: str | None = Field(
        None, description="Alternative or uncertain start date"
    )
    end_date_alt: str | None = Field(
        None, description="Alternative or uncertain end date"
    )


class RelationBase(BaseModel):
    """Defines a parental relationship between individuals."""

    relation_type: RelationType = Field(
        ..., description="Type of parental relationship"
    )
    parent1_id: int = Field(..., description="ID of the first parent")
    parent2_id: int = Field(..., description="ID of the second parent")


class IndividualBase(BaseModel):
    """Core representation of an individual in a genealogical base."""

    first_name: str = Field(..., description="Given name of the individual")
    last_name: str = Field(..., description="Family name of the individual")
    public_name: str | None = Field(
        None, description="Public or displayed name (e.g., 'J. Doe')"
    )

    image_url: str | None = Field(None, description="Profile or portrait URL")

    nickname: str | None = Field(None, description="Nickname of the individual")
    alias: str | None = Field(None, description="Alternative name or alias")
    alias_first_name: str | None = Field(None, description="Alternative given name")
    alias_last_name: str | None = Field(None, description="Alternative family name")

    profession: str | None = Field(None, description="Main profession or occupation")
    source: str | None = Field(
        None, description="Data source or reference for this individual"
    )

    number: int | None = Field(
        None, description="Numerical identifier (e.g., legacy system ID)"
    )
    gender: GenderType = Field(
        GenderType.UNKNOWN, description="Gender of the individual"
    )
    access_type_id: int | None = Field(
        None, description="Access restriction type or visibility level"
    )

    insert_nickname: bool = Field(
        False, description="Whether to insert nickname in display name"
    )
    insert_alias: bool = Field(
        False, description="Whether to insert alias in display name"
    )
    insert_firstname_alias: bool = Field(
        False, description="Whether to insert first name alias"
    )
    insert_lastname_alias: bool = Field(
        False, description="Whether to insert last name alias"
    )

    # --- Birth info ---
    birth_place: str | None = Field(None, description="Birthplace")
    birth_date1: str | None = Field(None, description="Primary birth date (ISO format)")
    birth_date_range: int | None = Field(
        None, description="Range between birth date1 and birth date2, in years"
    )
    birth_date2: str | None = Field(
        None, description="Alternative or secondary birth date"
    )
    birth_date3: str | None = Field(
        None, description="Tertiary birth date (e.g. for uncertainty)"
    )
    birth_notes: str | None = Field(None, description="Notes about the birth event")
    birth_source: str | None = Field(
        None, description="Source of the birth information"
    )
    birth_witnesses_ids: list[int] = Field(
        default_factory=list, description="List of IDs of birth witnesses"
    )

    # --- Baptism info ---
    baptism_place: str | None = Field(None, description="Baptism place")
    baptism_date1: str | None = Field(
        None, description="Primary baptism date (ISO format)"
    )
    baptism_date_range: int | None = Field(None, description="Date range for baptism")
    baptism_date2: str | None = Field(None, description="Secondary baptism date")
    baptism_date3: str | None = Field(None, description="Tertiary baptism date")
    baptism_notes: str | None = Field(None, description="Notes about the baptism event")
    baptism_source: str | None = Field(None, description="Source for baptism info")
    baptism_witnesses_ids: list[int] = Field(
        default_factory=list, description="IDs of baptism witnesses"
    )

    # --- Death info ---
    death_place: str | None = Field(None, description="Place of death")
    death_date1: str | None = Field(None, description="Primary death date (ISO format)")
    death_date_range: int | None = Field(
        None, description="Range between possible death dates, in years"
    )
    death_date2: str | None = Field(None, description="Secondary death date")
    death_date3: str | None = Field(None, description="Tertiary death date")
    death_notes: str | None = Field(None, description="Notes about death circumstances")
    death_source: str | None = Field(None, description="Source for death information")
    death_witnesses_ids: list[int] = Field(
        default_factory=list, description="IDs of death witnesses"
    )

    # --- Burial info ---
    burial_place: str | None = Field(None, description="Place of burial")
    burial_date1: str | None = Field(
        None, description="Primary burial date (ISO format)"
    )
    burial_date_range: int | None = Field(
        None, description="Range between burial dates, in years"
    )
    burial_date2: str | None = Field(None, description="Alternative burial date")
    burial_date3: str | None = Field(None, description="Tertiary burial date")
    burial_notes: str | None = Field(
        None, description="Notes about burial circumstances"
    )
    burial_source: str | None = Field(None, description="Source for burial information")
    burial_witnesses_ids: list[int] = Field(
        default_factory=list, description="IDs of burial witnesses"
    )

    # --- Relations & events ---
    events_ids: list[int] = Field(
        default_factory=list,
        description="List of event IDs associated with this individual",
    )
    relations_ids: list[int] = Field(
        default_factory=list,
        description="List of relation IDs associated with this individual",
    )
    title_ids: list[int] = Field(
        default_factory=list,
        description="List of title IDs associated with this individual",
    )

    notes: str | None = Field(None, description="General notes about the individual")


# ============================================================
#  Requests (inputs)
# ============================================================


class IndividualCreateRequest(IndividualBase):
    """Request schema for creating an individual."""

    pass


class IndividualGetRequest(BaseModel):
    """Request schema for retrieving an individual."""

    pass


class IndividualDeleteRequest(BaseModel):
    """Request schema for deleting an individual."""

    pass


# ============================================================
#  Responses (outputs)
# ============================================================


class IndividualCreateResponse(BaseModel):
    """Response schema after creating an individual."""

    individual_id: int = Field(..., description="Newly created individual ID")


class IndividualGetResponse(IndividualBase):
    """Response schema after retrieving an individual."""

    individual_id: int = Field(..., description="ID of the retrieved individual")


class IndividualDeleteResponse(BaseModel):
    """Response schema after deleting an individual."""

    success: bool = Field(
        True, description="Indicates if the individual was successfully deleted"
    )
    message: str | None = Field(
        None, description="Optional message about the operation result"
    )
