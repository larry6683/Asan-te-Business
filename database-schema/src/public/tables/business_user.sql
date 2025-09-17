
CREATE TABLE IF NOT EXISTS business_user(
    business_user_id                    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id                         UUID    NOT NULL,
    app_user_id                         UUID    NOT NULL,   
    business_user_permission_role_id    UUID    NOT NULL,

    FOREIGN KEY (business_id)                       REFERENCES business(business_id),
    FOREIGN KEY (app_user_id)                       REFERENCES app_user(app_user_id),
    FOREIGN KEY (business_user_permission_role_id)  REFERENCES business_user_permission_role(business_user_permission_role_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
