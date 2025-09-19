CREATE OR REPLACE PROCEDURE save_business_user_permission_role(
    code INT,
    business_user_permission_role_name TEXT
) 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO business_user_permission_role (code, business_user_permission_role_name)
    VALUES (code, business_user_permission_role_name)
    ON CONFLICT ON CONSTRAINT business_user_permission_role_code_key
    DO UPDATE 
        SET business_user_permission_role_name = EXCLUDED.business_user_permission_role_name;
END
$$;

/*
CALL save_business_user_permission_role(1, 'boop-business-permission-role');

SELECT  *
FROM    business_user_permission_role;
*/