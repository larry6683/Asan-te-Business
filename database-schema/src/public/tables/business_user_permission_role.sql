
CREATE TABLE IF NOT EXISTS business_user_permission_role
(
    business_user_permission_role_id    UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    code                                INT     NOT NULL UNIQUE,
    business_user_permission_role_name  TEXT    NOT NULL UNIQUE,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
