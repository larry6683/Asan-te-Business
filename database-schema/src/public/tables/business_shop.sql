
CREATE TABLE IF NOT EXISTS business_shop
(
    business_shop_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id         UUID    NOT NULL,
    shop_type_id        UUID    NOT NULL,
    shop_url            TEXT    NOT NULL,

    FOREIGN KEY (business_id)   REFERENCES business(business_id),
    FOREIGN KEY (shop_type_id)  REFERENCES shop_type(shop_type_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
