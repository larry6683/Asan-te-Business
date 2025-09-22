
CREATE TABLE IF NOT EXISTS user_type
(
    user_type_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code            INT     UNIQUE NOT NULL,
    user_type_name  TEXT    UNIQUE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
