CREATE TABLE family_event (
    family_id INTEGER NOT NULL REFERENCES family(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    PRIMARY KEY (family_id, event_id)
);
