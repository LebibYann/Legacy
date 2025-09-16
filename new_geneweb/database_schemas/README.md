# GeneWeb New Database Schema

## Overview
This directory defines a proposed relational schema for a new GeneWeb backend. It normalizes persons (individual), family units, events, titles, relationships between individuals, and witness roles attached to events.

Core tables:
- `individual`: Biographical core entity (names, birth/baptism/death/burial metadata, status flags, access control & gender, family link)
- `family`: Parental couple (optionally same-sex) linking mother/father to children (through `individual.family_id`)
- `relationship`: Generic interpersonal relationship (adoption, recognition, godparenting, foster, etc.) between two individuals
- `event`: Arbitrary dated place-associated event for an individual (custom extensible `event_name`)
- `title`: Nobility / honorific titles held by an individual over time
- `witness`: Participation of a third-party individual in an event with an assigned role

## Entity-Relationship Diagram
Mermaid visual graph of tables and their foreign-key connections:

```mermaid
erDiagram
    INDIVIDUAL ||--o{ FAMILY : "parents of"
    FAMILY ||--o{ INDIVIDUAL : "children"
    INDIVIDUAL ||--o{ EVENT : "has"
    INDIVIDUAL ||--o{ TITLE : "holds"
    INDIVIDUAL ||--o{ RELATIONSHIP : "as person1"
    INDIVIDUAL ||--o{ RELATIONSHIP : "as person2"
    EVENT ||--o{ WITNESS : "has"
    INDIVIDUAL ||--o{ WITNESS : "as subject"
    INDIVIDUAL ||--o{ WITNESS : "as witness"
```

Legend:
- Crow foot `o{` = zero or more; `||` = exactly one; `o|` would mean optional exactly one.
- Self references appear via multiple roles pointing back to `individual`.

## Table Notes & Cardinalities
- A `family` row optionally references up to two parent individuals (`father_id`, `mother_id`). A child links to at most one nuclear family via `individual.family_id`. (Extended/complex family or multiple unions would need an association table if required later.)
- `relationship` expresses pairwise links with a typed semantic meaning (`relationship_type_id`). Direction is significant only by convention; both `person1_id` and `person2_id` are required.
- `event` models personal life events (birth-like extras, migrations, occupations, religious, etc.). Additional normalized lookup tables could later replace free-text fields (e.g. place normalization).
- `witness` connects an `event` to third-party participants; one event may have many witnesses with distinct roles.
- `title` rows capture temporal intervals; overlapping entries possible (multiple contemporaneous titles).

## Enumerated/Domain Value Index
The schema stores several categorical attributes as integer codes. Below are their current dictionaries.

### gender_id
| id | label |
|----|-------|
| 0 | Unknown |
| 1 | Male |
| 2 | Female |

### access_type_id
| id | label |
|----|-------|
| 0 | If titles |
| 1 | Public |
| 2 | Public |

NOTE: Values 1 and 2 are identical; confirm whether 2 should instead represent a more restrictive classification (e.g. "Private" or "Restricted").

### death_status_id
| id | label |
|----|-------|
| 0 | Unknown |
| 1 | Alive |
| 2 | Dead |
| 3 | Dead as an infant |
| 4 | May be dead |

### death_kind
| id | label |
|----|-------|
| 0 | Killed |
| 1 | Murdered |
| 2 | Executed |
| 3 | Dissapeared |
| 4 | Unspecified |

(Spelling: consider `Disappeared`.)

### date_range (date qualifier semantics)
| id | label |
|----|-------|
| 0 | exact |
| 1 | about |
| 2 | possibly |
| 3 | before |
| 4 | after |
| 5 | ...or... |
| 6 | ...between... |

### role_id (witness roles)
| id | label |
|----|-------|
| 0 | Witness |
| 1 | Informant |
| 2 | Present |
| 3 | Cited |
| 4 | Civil registrar |
| 5 | Parish registrar |
| 6 | Other |

### relationship_type_id
| id | label |
|----|-------|
| 0 | Not specified |
| 1 | Adoptive parents |
| 2 | Recognized by |
| 3 | May be parents |
| 4 | Godparents |
| 5 | Foster parents |

## Suggested Normalization Enhancements
Future evolution could:
- Introduce lookup tables (`gender`, `death_status`, etc.) with FK constraints instead of inline integers for referential integrity and self-documentation.
- Add an associative `family_child` linking children to multiple parent-couple unions (supports complex genealogies, remarriages, blended families) instead of single `family_id` on `individual`.
- Factor place names into a `place` table with hierarchical geospatial normalization.
- Replace free-form `event_name` with an `event_type` reference table to unify semantics and allow localization.