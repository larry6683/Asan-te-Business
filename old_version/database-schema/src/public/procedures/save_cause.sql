CREATE OR REPLACE PROCEDURE save_cause(
    code INT,
    cause_name TEXT,
    cause_category_code INT
)
LANGUAGE plpgsql
AS $$
    DECLARE _cause_category_id UUID;
BEGIN

    SELECT  cc.cause_category_id INTO _cause_category_id
    FROM    cause_category AS cc
    WHERE   cc.code = cause_category_code
    LIMIT 1;

    IF _cause_category_id IS NULL THEN
        RAISE NOTICE 'no update: cause category with code (%) not found', cause_category_code;
        RETURN;
    END IF;

    INSERT INTO cause (cause_category_id, code, cause_name)
    VALUES 
        (_cause_category_id, code, cause_name)
    ON CONFLICT ON CONSTRAINT cause_code_key
    DO UPDATE
        SET cause_name = EXCLUDED.cause_name,
            cause_category_id = _cause_category_id;
END
$$;

/*
CALL save_cause(1, 'boop-cause', 1);

SELECT    c.cause_id,
        c.cause_category_id,
        c.code AS cause_code,
        c.cause_name,
        cc.code AS cause_category_code,
        cc.cause_category_name
FROM    cause AS c
JOIN    cause_category AS cc ON c.cause_category_id = cc.cause_category_id;
*/