CREATE TABLE event (
    id SERIAL PRIMARY KEY,                     -- Unique identifier for the event

    event_name TEXT NOT NULL,                  -- Event type (e.g. 'birth', 'death', 'marriage')
    place TEXT,                                -- Place of the event
    event_date_1 DATE,                         -- Start / main date
    event_date_2 DATE,                         -- Optional end date
    date_range INTEGER,                        -- Optional precision info (e.g. +/- years)
    notes TEXT,                                -- Notes about the event
    source TEXT,                               -- Source of information
    event_position INTEGER DEFAULT 0,          -- Optional ordering
);
