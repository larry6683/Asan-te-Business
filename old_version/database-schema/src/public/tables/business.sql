
CREATE TABLE IF NOT EXISTS business
(
    business_id             UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name           TEXT            UNIQUE NOT NULL,
    email                   TEXT            UNIQUE NOT NULL,
    website_url             TEXT,
    phone_number            TEXT,
    location_city           TEXT            NOT NULL,
    location_state          TEXT            NOT NULL,
    ein                     TEXT,
    business_description    VARCHAR(512)    NOT NULL    DEFAULT '',
    business_size_id        UUID            NOT NULL,
    business_name_hash      BYTEA           NULL,
    email_hash              BYTEA           NULL,

    FOREIGN KEY (business_size_id)  REFERENCES business_size(business_size_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS business_business_name_hash_idx  ON business USING HASH (business_name_hash);
CREATE INDEX IF NOT EXISTS business_email_hash_idx          ON business USING HASH (email_hash);
