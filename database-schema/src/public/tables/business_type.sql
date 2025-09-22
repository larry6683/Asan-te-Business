
CREATE TABLE IF NOT EXISTS business_type
(
    business_type_id   UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_type_name TEXT    NOT NULL,
    code               INT     NOT NULL UNIQUE,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
