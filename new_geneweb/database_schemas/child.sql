CREATE TABLE child (
    id SERIAL PRIMARY KEY,               -- Unique identifier for this child entry

    -- Foreign keys
    CONSTRAINT fk_child_family
        FOREIGN KEY (family_id) REFERENCES family(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_child_subject
        FOREIGN KEY (subject_id) REFERENCES individual(id)
        ON DELETE CASCADE,
);