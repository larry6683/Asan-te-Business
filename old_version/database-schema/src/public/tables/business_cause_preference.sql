
CREATE TABLE IF NOT EXISTS business_cause_preference
(
    business_cause_preference_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id                     UUID    NOT NULL,
    cause_id                        UUID    NOT NULL,
    cause_preference_rank_id        UUID    NOT NULL,

    FOREIGN KEY (business_id)               REFERENCES business(business_id),
    FOREIGN KEY (cause_id)                  REFERENCES cause(cause_id),
    FOREIGN KEY (cause_preference_rank_id)  REFERENCES cause_preference_rank(cause_preference_rank_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
