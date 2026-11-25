CREATE TABLE event (
    id SERIAL PRIMARY KEY,                     -- Unique identifier for the event
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,

    event_name TEXT NOT NULL,                  -- Event type (e.g. 'birth', 'death', 'marriage')
    place TEXT,                                -- Place of the event
    event_date_1 DATE,                         -- Start / main date
    event_date_2 DATE,                         -- Optional end date
    date_range INTEGER,                        -- Optional precision info (e.g. +/- years)
    notes TEXT,                                -- Notes about the event
    source TEXT,                               -- Source of information
    event_position INTEGER DEFAULT 0,          -- Optional ordering

    -- Foreign keys
    CONSTRAINT fk_event_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_event_database_id ON event(database_id);
