CREATE TABLE family_event (
    family_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    
    PRIMARY KEY (family_id, event_id),
    
    -- Foreign keys
    CONSTRAINT fk_family_event_family
        FOREIGN KEY (family_id) REFERENCES family(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_family_event_event
        FOREIGN KEY (event_id) REFERENCES event(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_family_event_event_id ON family_event(event_id);
