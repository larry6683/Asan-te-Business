
CREATE TABLE IF NOT EXISTS social_media_type
(

    social_media_type_id       UUID   PRIMARY KEY DEFAULT gen_random_uuid(),
    code                       INT    UNIQUE NOT NULL,
    social_media_type_name     TEXT   UNIQUE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
