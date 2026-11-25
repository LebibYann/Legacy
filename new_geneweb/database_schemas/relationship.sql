CREATE TABLE relationship (
    id SERIAL PRIMARY KEY,                -- Unique identifier for this relationship record
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,

    person1_id INTEGER NOT NULL,          -- First individual
    person2_id INTEGER NOT NULL,          -- Second individual
    relationship_type_id INTEGER NOT NULL DEFAULT 0,

    person1_may_be_dead BOOLEAN DEFAULT FALSE,
    person2_may_be_dead BOOLEAN DEFAULT FALSE,

    person1_public BOOLEAN DEFAULT FALSE,
    person2_public BOOLEAN DEFAULT FALSE,

    -- Foreign keys
    CONSTRAINT fk_relationship_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_relationship_person1
        FOREIGN KEY (person1_id) REFERENCES individual(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_relationship_person2
        FOREIGN KEY (person2_id) REFERENCES individual(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_relationship_database_id ON relationship(database_id);
CREATE INDEX idx_relationship_person1_id ON relationship(person1_id);
CREATE INDEX idx_relationship_person2_id ON relationship(person2_id);
