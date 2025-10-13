
CREATE TABLE IF NOT EXISTS beneficiary_user(
    beneficiary_user_id                     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    beneficiary_id                          UUID    NOT NULL,
    app_user_id                             UUID    NOT NULL,   
    beneficiary_user_permission_role_id     UUID    NOT NULL,

    FOREIGN KEY (beneficiary_id)                        REFERENCES beneficiary(beneficiary_id),
    FOREIGN KEY (app_user_id)                           REFERENCES app_user(app_user_id),
    FOREIGN KEY (beneficiary_user_permission_role_id)   REFERENCES beneficiary_user_permission_role(beneficiary_user_permission_role_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
