
CREATE TABLE IF NOT EXISTS cause 
(
    cause_id            UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code                INT     UNIQUE NOT NULL,
    cause_name          TEXT    UNIQUE NOT NULL,
    
    cause_category_id   UUID    REFERENCES cause_category(cause_category_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
