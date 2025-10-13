
CREATE TABLE IF NOT EXISTS shop_type
(
    shop_type_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code            INT     NOT NULL UNIQUE,
    shop_type_name  TEXT    NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
