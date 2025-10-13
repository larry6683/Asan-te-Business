
CREATE TABLE IF NOT EXISTS beneficiary_shop
(
    beneficiary_shop_id     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    beneficiary_id          UUID    NOT NULL,
    shop_type_id            UUID    NOT NULL,
    shop_url                TEXT    NOT NULL,

    FOREIGN KEY (beneficiary_id)    REFERENCES beneficiary(beneficiary_id),
    FOREIGN KEY (shop_type_id)      REFERENCES shop_type(shop_type_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
