
CREATE TABLE IF NOT EXISTS beneficiary_type
(
    beneficiary_type_id   UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    beneficiary_type_name TEXT    NOT NULL,
    code                  INT     NOT NULL UNIQUE,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
