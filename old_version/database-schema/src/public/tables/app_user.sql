
CREATE TABLE IF NOT EXISTS app_user
(
    app_user_id             UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_type_id            UUID    NOT NULL,
    email                   TEXT    NOT NULL,
    mailing_list_signup     BOOL    NOT NULL DEFAULT FALSE,
    email_hash              BYTEA   NULL,

    FOREIGN KEY (user_type_id)  REFERENCES user_type(user_type_id),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS app_user_email_hash_idx ON app_user USING HASH (email_hash);
