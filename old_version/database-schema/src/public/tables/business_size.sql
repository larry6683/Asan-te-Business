
CREATE TABLE IF NOT EXISTS business_size
(
    business_size_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code                INT     UNIQUE NOT NULL,
    business_size_name  TEXT    UNIQUE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
