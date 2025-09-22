
CREATE TABLE IF NOT EXISTS business_impact_link
(
    business_impact_link_id     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id                 UUID    NOT NULL,
    impact_link_url             TEXT    NOT NULL,

    FOREIGN KEY (business_id)   REFERENCES business(business_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
