CREATE TABLE event (
    id SERIAL PRIMARY KEY,               -- Unique identifier for the event
    individual_id INTEGER NOT NULL,      -- Person involved in this event
    event_id INTEGER,
    event_name TEXT,                     -- Event type (customizable)
    event_position INTEGER DEFAULT 0,
    place TEXT,                          -- Place of the event
    event_date_1 DATE,                   -- Date of the event
    date_range INTEGER,
    event_date_2 DATE,                   -- Date of the event
    event_date_3 TEXT,                   -- Date of the event
    notes TEXT,                          -- Notes about the event
    source TEXT,                         -- Source of the information

    -- Foreign key linking to the individual
    CONSTRAINT fk_event_individual
        FOREIGN KEY (individual_id) REFERENCES individual(id)
        ON DELETE CASCADE
);