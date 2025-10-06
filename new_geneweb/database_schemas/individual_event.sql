CREATE TABLE individual_event (
    individual_id INTEGER NOT NULL REFERENCES individual(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    PRIMARY KEY (individual_id, event_id)
);
