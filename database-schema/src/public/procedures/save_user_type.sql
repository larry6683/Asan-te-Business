CREATE OR REPLACE PROCEDURE save_user_type(
    code INT,
    user_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO user_type (code, user_type_name)
    VALUES (code, user_type_name)
    ON CONFLICT ON CONSTRAINT user_type_code_key
    DO UPDATE
        SET user_type_name = EXCLUDED.user_type_name;
END;
$$;