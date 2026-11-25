CREATE TABLE witness (
    id SERIAL PRIMARY KEY,               -- Unique identifier for this witness entry
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,

    event_id INTEGER NOT NULL,           -- Related event
    subject_id INTEGER NOT NULL,         -- Person experiencing the event
    witness_id INTEGER NOT NULL,         -- Person acting as a witness
    role_id INTEGER DEFAULT 0,           -- Role of the witness (see dict below)

    occupation TEXT,                     -- Occupation of the witness
    number INTEGER DEFAULT 0,            -- Reference number (optional)

    gender_id INTEGER DEFAULT 0,         -- Sex of the witness (see dict below)
    may_be_dead BOOLEAN DEFAULT FALSE,   -- Whether the witness may be dead
    is_public BOOLEAN DEFAULT FALSE,     -- Whether the witness information is public

    -- Foreign keys
    CONSTRAINT fk_witness_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_witness_event
        FOREIGN KEY (event_id) REFERENCES event(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_witness_subject
        FOREIGN KEY (subject_id) REFERENCES individual(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_witness_person
        FOREIGN KEY (witness_id) REFERENCES individual(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_witness_database_id ON witness(database_id);
CREATE INDEX idx_witness_event_id ON witness(event_id);
CREATE INDEX idx_witness_subject_id ON witness(subject_id);
CREATE INDEX idx_witness_witness_id ON witness(witness_id);
