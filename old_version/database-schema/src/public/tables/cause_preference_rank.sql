
CREATE TABLE IF NOT EXISTS cause_preference_rank
(
    cause_preference_rank_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code                        INT     NOT NULL UNIQUE,
    cause_preference_rank_name  TEXT    NOT NULL UNIQUE,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
