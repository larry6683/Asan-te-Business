CREATE OR REPLACE PROCEDURE save_beneficiary_size(
    code INT,
    beneficiary_size_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO beneficiary_size (code, beneficiary_size_name)
    VALUES (code, beneficiary_size_name)
    ON CONFLICT ON CONSTRAINT beneficiary_size_code_key
    DO UPDATE
        SET beneficiary_size_name = EXCLUDED.beneficiary_size_name;
END
$$;

/*
CALL save_beneficiary_size(1, 'boop-beneficiary-size');

SELECT  *
FROM    beneficiary_size;
*/