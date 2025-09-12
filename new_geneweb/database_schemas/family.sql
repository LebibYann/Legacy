CREATE TABLE family (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for this family

    father_id INTEGER,                     -- ID of the father (NULL if not known)
    mother_id INTEGER,                     -- ID of the mother (NULL if not known)
    same_sex_couple BOOLEAN DEFAULT FALSE, -- True if this is a same-sex couple

    source_individuals TEXT,               -- Sources for individuals
    source_family TEXT,                    -- Sources for the family
    comment TEXT,                          -- Additional comments

    -- Foreign keys
    CONSTRAINT fk_family_father
        FOREIGN KEY (father_id) REFERENCES individual(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_family_mother
        FOREIGN KEY (mother_id) REFERENCES individual(id)
        ON DELETE SET NULL
);