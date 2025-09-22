CREATE OR REPLACE PROCEDURE save_cause_category(
    code INT,
    cause_category_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO cause_category (code, cause_category_name)
    VALUES (code, cause_category_name)
    ON CONFLICT ON CONSTRAINT cause_category_code_key
    DO UPDATE
        SET cause_category_name = EXCLUDED.cause_category_name;
END
$$;

/*
CALL save_cause_category(1, 'boop-cause-category');

SELECT  *
FROM    cause_category;
*/