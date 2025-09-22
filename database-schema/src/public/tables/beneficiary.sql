
CREATE TABLE IF NOT EXISTS beneficiary
(
    beneficiary_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    beneficiary_name        TEXT            UNIQUE NOT NULL,
    email                   TEXT            UNIQUE NOT NULL,
    website_url             TEXT,
    phone_number            TEXT,
    location_city           TEXT            NOT NULL,
    location_state          TEXT            NOT NULL,
    ein                     TEXT,
    beneficiary_description VARCHAR(512)    NOT NULL    DEFAULT '',
    beneficiary_size_id     UUID            NOT NULL,
    beneficiary_name_hash   BYTEA           NULL,
    email_hash              BYTEA           NULL,

    FOREIGN KEY (beneficiary_size_id)   REFERENCES beneficiary_size(beneficiary_size_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS beneficiary_beneficiary_name_hash_idx    ON beneficiary  USING HASH (beneficiary_name_hash);
CREATE INDEX IF NOT EXISTS beneficiary_email_hash_idx               ON beneficiary  USING HASH (email_hash);
