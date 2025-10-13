CREATE OR REPLACE PROCEDURE save_beneficiary_user_permission_role(
    code INT,
    beneficiary_user_permission_role_name TEXT
) 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO beneficiary_user_permission_role (code, beneficiary_user_permission_role_name)
    VALUES (code, beneficiary_user_permission_role_name)
    ON CONFLICT ON CONSTRAINT beneficiary_user_permission_role_code_key
    DO UPDATE 
        SET beneficiary_user_permission_role_name = EXCLUDED.beneficiary_user_permission_role_name;
        
END
$$;

/*
CALL save_beneficiary_user_permission_role(1, 'boop-beneficiary-permission-role');

SELECT  *
FROM    beneficiary_user_permission_role;
*/