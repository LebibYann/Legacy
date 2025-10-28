CREATE TABLE individual (
    id SERIAL PRIMARY KEY,
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,

    -- Basic information
    first_name TEXT,
    last_name TEXT,
    public_name TEXT,

    image_url TEXT,

    nickname TEXT,
    alias TEXT,
    alias_first_name TEXT,
    alias_last_name TEXT,

    professions TEXT,
    source TEXT,

    number INTEGER DEFAULT 0,
    gender_id INTEGER DEFAULT 0,
    access_type_id INTEGER DEFAULT 0,

    insert_nickname BOOLEAN DEFAULT FALSE,
    insert_alias BOOLEAN DEFAULT FALSE,
    insert_firstname_alias BOOLEAN DEFAULT FALSE,
    insert_lastname_alias BOOLEAN DEFAULT FALSE,

    -- Birth
    birth_place TEXT,
    birth_date_1 DATE,
    birth_date_range INTEGER,
    birth_date_2 DATE,
    birth_date_3 TEXT,
    birth_notes TEXT,
    birth_source TEXT,

    -- Baptism
    baptism_place TEXT,
    baptism_date_1 DATE,
    baptism_date_range INTEGER,
    baptism_date_2 DATE,
    baptism_date_3 TEXT,
    baptism_notes TEXT,
    baptism_source TEXT,

    -- Death
    death_status_id INTEGER DEFAULT 0,
    death_kind INTEGER,

    death_place TEXT,
    death_date_1 DATE,
    death_date_range INTEGER,
    death_date_2 DATE,
    death_date_3 TEXT,
    death_notes TEXT,
    death_source TEXT,

    -- Burial
    burial_place TEXT,
    burial_date_1 DATE,
    burial_date_range INTEGER,
    burial_date_2 DATE,
    burial_date_3 TEXT,
    burial_notes TEXT,
    burial_source TEXT,

    -- Free notes
    notes TEXT,

    -- Foreign keys
    CONSTRAINT fk_individual_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE
);

-- Index for performance (database_id is critical for multi-database queries)
CREATE INDEX idx_individual_database_id ON individual(database_id);
