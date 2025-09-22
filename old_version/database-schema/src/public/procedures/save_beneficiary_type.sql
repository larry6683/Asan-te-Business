CREATE OR REPLACE PROCEDURE save_beneficiary_type(
    code INT,
    beneficiary_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO beneficiary_type (code, beneficiary_type_name)
    VALUES (code, beneficiary_type_name)
    ON CONFLICT ON CONSTRAINT beneficiary_type_code_key
    DO UPDATE 
        SET beneficiary_type_name = EXCLUDED.beneficiary_type_name;
END
$$;

/*
CALL save_beneficiary_type(1, 'non-profit');

SELECT *
FROM beneficiary_type;
*/
