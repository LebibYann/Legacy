CREATE TABLE geneweb_database (
    id SERIAL PRIMARY KEY,                -- Unique identifier for this database
    
    name TEXT NOT NULL UNIQUE,            -- Database name (must be unique)
    description TEXT,                      -- Optional description
    created_at TIMESTAMP DEFAULT NOW(),    -- Creation timestamp
    updated_at TIMESTAMP DEFAULT NOW(),    -- Last update timestamp
    is_active BOOLEAN DEFAULT TRUE,        -- Whether this database is active
    
    -- Metadata
    owner TEXT,                            -- Owner of the database
    access_level INTEGER DEFAULT 1,        -- Access level (0=private, 1=public, 2=restricted)
    
    -- Statistics (optional, can be computed)
    individual_count INTEGER DEFAULT 0,    -- Number of individuals
    family_count INTEGER DEFAULT 0         -- Number of families
);

-- Index for performance
CREATE INDEX idx_geneweb_database_name ON geneweb_database(name);
CREATE INDEX idx_geneweb_database_active ON geneweb_database(is_active);
