"""
SQLAlchemy models for GeneWeb database.
Based on the SQL schemas defined in database_schemas/
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class GenewebDatabase(Base):
    """
    Root table for multi-database support.
    Based on database_schemas/geneweb_database.sql
    """

    __tablename__ = "geneweb_database"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database information
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Metadata
    owner: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    access_level: Mapped[int] = mapped_column(Integer, default=1)

    # Statistics
    individual_count: Mapped[int] = mapped_column(Integer, default=0)
    family_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    individuals: Mapped[list["Individual"]] = relationship(
        "Individual", back_populates="database", cascade="all, delete-orphan"
    )
    families: Mapped[list["Family"]] = relationship(
        "Family", back_populates="database", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="database", cascade="all, delete-orphan"
    )
    relationships: Mapped[list["Relationship"]] = relationship(
        "Relationship", back_populates="database", cascade="all, delete-orphan"
    )
    titles: Mapped[list["Title"]] = relationship(
        "Title", back_populates="database", cascade="all, delete-orphan"
    )
    witnesses: Mapped[list["Witness"]] = relationship(
        "Witness", back_populates="database", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<GenewebDatabase(id={self.id}, name='{self.name}')>"


class Individual(Base):
    """
    Individual person in the genealogical database.
    Based on database_schemas/individual.sql
    """

    __tablename__ = "individual"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # Basic information
    first_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    public_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    nickname: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias_first_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias_last_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    professions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status fields
    number: Mapped[int] = mapped_column(Integer, default=0)
    gender_id: Mapped[int] = mapped_column(Integer, default=0)
    access_type_id: Mapped[int] = mapped_column(Integer, default=0)

    # Boolean flags
    insert_nickname: Mapped[bool] = mapped_column(Boolean, default=False)
    insert_alias: Mapped[bool] = mapped_column(Boolean, default=False)
    insert_firstname_alias: Mapped[bool] = mapped_column(Boolean, default=False)
    insert_lastname_alias: Mapped[bool] = mapped_column(Boolean, default=False)

    # Birth information
    birth_place: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birth_date_1: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    birth_date_range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    birth_date_2: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    birth_date_3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birth_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birth_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Baptism information
    baptism_place: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    baptism_date_1: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    baptism_date_range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    baptism_date_2: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    baptism_date_3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    baptism_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    baptism_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Death information
    death_status_id: Mapped[int] = mapped_column(Integer, default=0)
    death_kind: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    death_place: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    death_date_1: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    death_date_range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    death_date_2: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    death_date_3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    death_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    death_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Burial information
    burial_place: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    burial_date_1: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    burial_date_range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    burial_date_2: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    burial_date_3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    burial_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    burial_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Free notes
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="individuals"
    )
    father_families: Mapped[list["Family"]] = relationship(
        "Family", foreign_keys="Family.father_id", back_populates="father"
    )
    mother_families: Mapped[list["Family"]] = relationship(
        "Family", foreign_keys="Family.mother_id", back_populates="mother"
    )
    child_links: Mapped[list["Child"]] = relationship(
        "Child", back_populates="child_individual", cascade="all, delete-orphan"
    )
    individual_events: Mapped[list["IndividualEvent"]] = relationship(
        "IndividualEvent", back_populates="individual", cascade="all, delete-orphan"
    )
    titles: Mapped[list["Title"]] = relationship(
        "Title", back_populates="individual", cascade="all, delete-orphan"
    )
    relationships_as_person1: Mapped[list["Relationship"]] = relationship(
        "Relationship", foreign_keys="Relationship.person1_id", back_populates="person1"
    )
    relationships_as_person2: Mapped[list["Relationship"]] = relationship(
        "Relationship", foreign_keys="Relationship.person2_id", back_populates="person2"
    )
    witness_roles: Mapped[list["Witness"]] = relationship(
        "Witness", foreign_keys="Witness.witness_id", back_populates="witness"
    )
    subject_witnesses: Mapped[list["Witness"]] = relationship(
        "Witness", foreign_keys="Witness.subject_id", back_populates="subject"
    )

    def __repr__(self) -> str:
        return f"<Individual(id={self.id}, name='{self.first_name} {self.last_name}')>"


class Family(Base):
    """
    Family unit linking parents and children.
    Based on database_schemas/family.sql
    """

    __tablename__ = "family"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # Parent references
    father_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="SET NULL"), nullable=True
    )
    mother_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="SET NULL"), nullable=True
    )

    # Family characteristics
    same_sex_couple: Mapped[bool] = mapped_column(Boolean, default=False)

    # Sources and comments
    source_individuals: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_family: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="families"
    )
    father: Mapped[Optional["Individual"]] = relationship(
        "Individual", foreign_keys=[father_id], back_populates="father_families"
    )
    mother: Mapped[Optional["Individual"]] = relationship(
        "Individual", foreign_keys=[mother_id], back_populates="mother_families"
    )
    child_links: Mapped[list["Child"]] = relationship(
        "Child", back_populates="family", cascade="all, delete-orphan"
    )
    family_events: Mapped[list["FamilyEvent"]] = relationship(
        "FamilyEvent", back_populates="family", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Family(id={self.id}, father_id={self.father_id}, mother_id={self.mother_id})>"


class Event(Base):
    """
    Arbitrary dated events with locations.
    Based on database_schemas/event.sql
    """

    __tablename__ = "event"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # Event details
    event_name: Mapped[str] = mapped_column(Text, nullable=False)
    place: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    event_position: Mapped[int] = mapped_column(Integer, default=0)

    # Date information
    event_date_1: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    event_date_2: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Additional information
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="events"
    )
    individual_events: Mapped[list["IndividualEvent"]] = relationship(
        "IndividualEvent", back_populates="event", cascade="all, delete-orphan"
    )
    family_events: Mapped[list["FamilyEvent"]] = relationship(
        "FamilyEvent", back_populates="event", cascade="all, delete-orphan"
    )
    witnesses: Mapped[list["Witness"]] = relationship(
        "Witness", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, name='{self.event_name}')>"


class Relationship(Base):
    """
    Relationships between individuals.
    Based on database_schemas/relationship.sql
    """

    __tablename__ = "relationship"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # Person references
    person1_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )
    person2_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )

    # Relationship type
    relationship_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    # Status flags
    person1_may_be_dead: Mapped[bool] = mapped_column(Boolean, default=False)
    person2_may_be_dead: Mapped[bool] = mapped_column(Boolean, default=False)
    person1_public: Mapped[bool] = mapped_column(Boolean, default=False)
    person2_public: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="relationships"
    )
    person1: Mapped["Individual"] = relationship(
        "Individual",
        foreign_keys=[person1_id],
        back_populates="relationships_as_person1",
    )
    person2: Mapped["Individual"] = relationship(
        "Individual",
        foreign_keys=[person2_id],
        back_populates="relationships_as_person2",
    )

    def __repr__(self) -> str:
        return f"<Relationship(id={self.id}, person1_id={self.person1_id}, person2_id={self.person2_id}, type={self.relationship_type_id})>"


class Title(Base):
    """
    Titles held by individuals.
    Based on database_schemas/title.sql
    """

    __tablename__ = "title"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # Individual reference
    individual_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )

    # Title information
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fief: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rank: Mapped[int] = mapped_column(Integer, default=0)
    main_title: Mapped[bool] = mapped_column(Boolean, default=False)

    # Date range
    begin_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    begin_date_alt: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date_alt: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="titles"
    )
    individual: Mapped["Individual"] = relationship(
        "Individual", back_populates="titles"
    )

    def __repr__(self) -> str:
        return f"<Title(id={self.id}, individual_id={self.individual_id}, title='{self.title}')>"


class Witness(Base):
    """
    Witnesses for events.
    Based on database_schemas/witness.sql
    """

    __tablename__ = "witness"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Database reference (REQUIRED for multi-database support)
    database_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("geneweb_database.id", ondelete="CASCADE"), nullable=False
    )

    # References
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )
    witness_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )

    # Witness details
    role_id: Mapped[int] = mapped_column(Integer, default=0)
    occupation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    number: Mapped[int] = mapped_column(Integer, default=0)

    # Status flags
    gender_id: Mapped[int] = mapped_column(Integer, default=0)
    may_be_dead: Mapped[bool] = mapped_column(Boolean, default=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    database: Mapped["GenewebDatabase"] = relationship(
        "GenewebDatabase", back_populates="witnesses"
    )
    event: Mapped["Event"] = relationship("Event", back_populates="witnesses")
    subject: Mapped["Individual"] = relationship(
        "Individual", foreign_keys=[subject_id], back_populates="subject_witnesses"
    )
    witness: Mapped["Individual"] = relationship(
        "Individual", foreign_keys=[witness_id], back_populates="witness_roles"
    )

    def __repr__(self) -> str:
        return f"<Witness(id={self.id}, event_id={self.event_id}, witness_id={self.witness_id}, role={self.role_id})>"


class Child(Base):
    """
    Association table linking families to their children.
    Based on database_schemas/child.sql
    """

    __tablename__ = "child"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    family_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("family.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    family: Mapped["Family"] = relationship("Family", back_populates="child_links")
    child_individual: Mapped["Individual"] = relationship(
        "Individual", back_populates="child_links"
    )

    def __repr__(self) -> str:
        return f"<Child(id={self.id}, family_id={self.family_id}, subject_id={self.subject_id})>"


class IndividualEvent(Base):
    """
    Association table linking individuals to events.
    Based on database_schemas/individual_event.sql
    """

    __tablename__ = "individual_event"

    # Composite primary key
    individual_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("individual.id", ondelete="CASCADE"), primary_key=True
    )
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    individual: Mapped["Individual"] = relationship(
        "Individual", back_populates="individual_events"
    )
    event: Mapped["Event"] = relationship("Event", back_populates="individual_events")

    def __repr__(self) -> str:
        return f"<IndividualEvent(individual_id={self.individual_id}, event_id={self.event_id})>"


class FamilyEvent(Base):
    """
    Association table linking families to events.
    Based on database_schemas/family_event.sql
    """

    __tablename__ = "family_event"

    # Composite primary key
    family_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("family.id", ondelete="CASCADE"), primary_key=True
    )
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    family: Mapped["Family"] = relationship("Family", back_populates="family_events")
    event: Mapped["Event"] = relationship("Event", back_populates="family_events")

    def __repr__(self) -> str:
        return f"<FamilyEvent(family_id={self.family_id}, event_id={self.event_id})>"
