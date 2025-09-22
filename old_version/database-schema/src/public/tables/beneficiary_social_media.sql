
CREATE TABLE IF NOT EXISTS beneficiary_social_media
(
    beneficiary_social_media_id     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    beneficiary_id                  UUID    NOT NULL,
    social_media_type_id            UUID    NOT NULL,
    social_media_url                TEXT    UNIQUE NOT NULL,
    
    FOREIGN KEY (beneficiary_id)        REFERENCES beneficiary(beneficiary_id),
    FOREIGN KEY (social_media_type_id)  REFERENCES social_media_type(social_media_type_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
