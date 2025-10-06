CREATE TABLE child (
    id SERIAL PRIMARY KEY,               -- Unique identifier for this child entry
    
    family_id INTEGER NOT NULL,          -- Family to which this child belongs
    subject_id INTEGER NOT NULL,         -- Individual who is the child

    -- Foreign keys
    CONSTRAINT fk_child_family
        FOREIGN KEY (family_id) REFERENCES family(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_child_subject
        FOREIGN KEY (subject_id) REFERENCES individual(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_child_family_id ON child(family_id);
CREATE INDEX idx_child_subject_id ON child(subject_id);
