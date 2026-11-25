CREATE TABLE title (
    id SERIAL PRIMARY KEY,                -- Unique identifier for this title
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,
    
    individual_id INTEGER NOT NULL,       -- Person holding this title

    title TEXT,                           -- Title (e.g., Duke, Baron)
    name TEXT,                            -- Full name of the title (e.g., Duke of Normandy)
    fief TEXT,                            -- Associated fief
    rank INTEGER DEFAULT 0,               -- Rank (0 if not specified)
    main_title BOOLEAN DEFAULT FALSE,     -- Whether this is the main title

    begin_date DATE,                      -- Start date of the title
    end_date DATE,                        -- End date of the title
    begin_date_alt DATE,                  -- Alternative/approx start date
    end_date_alt DATE,                    -- Alternative/approx end date

    -- Foreign keys
    CONSTRAINT fk_title_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_title_individual
        FOREIGN KEY (individual_id) REFERENCES individual(id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_title_database_id ON title(database_id);
CREATE INDEX idx_title_individual_id ON title(individual_id);
