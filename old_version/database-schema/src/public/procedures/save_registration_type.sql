CREATE OR REPLACE PROCEDURE save_registration_type(
    code INT,
    registration_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO registration_type (code, registration_type_name)
    VALUES (code, registration_type_name)
    ON CONFLICT ON CONSTRAINT registration_type_code_key
    DO UPDATE 
        SET registration_type_name = EXCLUDED.registration_type_name;
END
$$;

/*
CALL save_registration_type(1, 'business');
CALL save_registration_type(2, 'non-profit');
CALL save_registration_type(3, 'consumer');

SELECT *
FROM registration_type;
*/
