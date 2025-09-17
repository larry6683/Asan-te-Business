
CREATE TABLE IF NOT EXISTS beneficiary_size
(
    beneficiary_size_id     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code                    INT     UNIQUE NOT NULL, 
    beneficiary_size_name   TEXT    UNIQUE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
