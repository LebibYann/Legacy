CREATE TABLE individual_event (
    individual_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    
    PRIMARY KEY (individual_id, event_id),
    
    -- Foreign keys
    CONSTRAINT fk_individual_event_individual
        FOREIGN KEY (individual_id) REFERENCES individual(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_individual_event_event
        FOREIGN KEY (event_id) REFERENCES event(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_individual_event_event_id ON individual_event(event_id);
