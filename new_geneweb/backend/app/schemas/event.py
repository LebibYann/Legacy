from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

# ============================================================
# Enumerations
# ============================================================


class EventIndividualType(str, Enum):
    """Possible event types for individual-related events."""

    ACCOMPLISHMENT = "Accomplishment"
    ACQUISITION = "Acquisition"
    BARMITZVAH = "Bar Mitzvah"
    BATMITZVAH = "Bat Mitzvah"
    BENEDICTION = "Benediction"
    CUSTOM = "Custom"
    # TODO: complete the list of individual event types


class EventFamilyType(str, Enum):
    """Possible event types for family-related events."""

    MARRIAGE = "Marriage"
    NOT_MARRIED = "Not Married"
    ENGAGEMENT = "Engagement"
    NO_MENTION = "No Mention"
    MARRIAGE_BANN = "Marriage Bann"
    MARRIAGE_CONTRACT = "Marriage Contract"
    MARRIAGE_LICENSE = "Marriage License"
    CIVIL_MARRIAGE = "Civil Marriage"
    DIVORCE = "Divorce"
    SEPARATION = "Separation"
    ANNULMENT = "Annulment"
    RESIDENCE = "Residence"
    CUSTOM = "Custom"


# ============================================================
# Base schema (shared by all requests & responses)
# ============================================================


class EventBase(BaseModel):
    """Base structure for any genealogical event."""

    base_id: int = Field(..., description="ID of the base where this event is stored")

    place: str | None = Field(None, description="Place where the event occurred")
    event_date1: str | None = Field(
        None, description="Primary date associated with the event (ISO format)"
    )
    event_date2: str | None = Field(
        None, description="Secondary date, if applicable (ISO format)"
    )
    date_range: int | None = Field(
        None, description="Date range (in years) between event_date1 and event_date2"
    )
    note: str | None = Field(None, description="Additional notes about the event")
    source: str | None = Field(None, description="Source of the event information")
    event_position: int | None = Field(
        None, description="Position/order index of the event within a record"
    )
    custom_field: str | None = Field(None, description="Custom user-defined event data")


class EventIndividualBase(EventBase):
    """Base schema for individual events."""

    event_type: EventIndividualType = Field(
        default=EventIndividualType.ACCOMPLISHMENT,
        description="Type of the individual event",
    )
    individual_id: int | None = Field(None, description="ID of the related individual")


class EventFamilyBase(EventBase):
    """Base schema for family events."""

    event_type: EventFamilyType = Field(
        default=EventFamilyType.MARRIAGE,
        description="Type of the family event",
    )
    family_id: int | None = Field(None, description="ID of the related family")
