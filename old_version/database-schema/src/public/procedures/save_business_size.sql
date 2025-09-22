CREATE OR REPLACE PROCEDURE save_business_size(
    code INT,
    business_size_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO business_size (code, business_size_name)
    VALUES (code, business_size_name)
    ON CONFLICT ON CONSTRAINT business_size_code_key
    DO UPDATE
        SET business_size_name = EXCLUDED.business_size_name;
END
$$;

/*
CALL save_business_size(1, 'boop-business-size');

SELECT  *
FROM    business_size;
*/