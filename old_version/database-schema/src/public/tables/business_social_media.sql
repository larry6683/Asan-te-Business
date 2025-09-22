
CREATE TABLE IF NOT EXISTS business_social_media
(
    business_social_media_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id                 UUID    NOT NULL,
    social_media_type_id        UUID    NOT NULL,
    social_media_url            TEXT    NOT NULL,

    FOREIGN KEY (business_id)          REFERENCES business(business_id),
    FOREIGN KEY (social_media_type_id) REFERENCES social_media_type(social_media_type_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
