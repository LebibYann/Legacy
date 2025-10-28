CREATE TABLE family (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for this family
    
    -- Database reference (REQUIRED for multi-database support)
    database_id INTEGER NOT NULL,

    father_id INTEGER,                     -- ID of the father (NULL if not known)
    mother_id INTEGER,                     -- ID of the mother (NULL if not known)
    same_sex_couple BOOLEAN DEFAULT FALSE, -- True if this is a same-sex couple

    source_individuals TEXT,               -- Sources for individuals
    source_family TEXT,                    -- Sources for the family
    comment TEXT,                          -- Additional comments

    -- Foreign keys
    CONSTRAINT fk_family_database
        FOREIGN KEY (database_id) REFERENCES geneweb_database(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_family_father
        FOREIGN KEY (father_id) REFERENCES individual(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_family_mother
        FOREIGN KEY (mother_id) REFERENCES individual(id)
        ON DELETE SET NULL
);

-- Index for performance
CREATE INDEX idx_family_database_id ON family(database_id);
CREATE INDEX idx_family_father_id ON family(father_id);
CREATE INDEX idx_family_mother_id ON family(mother_id);
