CREATE OR REPLACE PROCEDURE save_business_type(
    code INT,
    business_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO business_type (code, business_type_name)
    VALUES (code, business_type_name)
    ON CONFLICT ON CONSTRAINT business_type_code_key
    DO UPDATE 
        SET business_type_name = EXCLUDED.business_type_name;
END
$$;

/*
CALL save_business_type(1, 'business');

SELECT *
FROM business_type;
*/
