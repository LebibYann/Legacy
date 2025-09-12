CREATE TABLE relationship (
    id SERIAL PRIMARY KEY,                -- Unique identifier for this relationship record

    person1_id INTEGER NOT NULL,          -- First individual
    person2_id INTEGER NOT NULL,          -- Second individual
    relationship_type_id INTEGER NOT NULL DEFAULT 0,

    person1_may_be_dead BOOLEAN DEFAULT FALSE,
    person2_may_be_dead BOOLEAN DEFAULT FALSE,

    person1_public BOOLEAN DEFAULT FALSE,
    person2_public BOOLEAN DEFAULT FALSE,

    -- Foreign keys
    CONSTRAINT fk_relationship_person1
        FOREIGN KEY (person1_id) REFERENCES individual(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_relationship_person2
        FOREIGN KEY (person2_id) REFERENCES individual(id)
        ON DELETE CASCADE
);