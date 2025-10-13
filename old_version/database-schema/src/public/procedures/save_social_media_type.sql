CREATE OR REPLACE PROCEDURE save_social_media_type(
    code INT,
    social_media_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO social_media_type (code, social_media_type_name)
    VALUES (code, social_media_type_name)
    ON CONFLICT ON CONSTRAINT social_media_type_code_key
    DO UPDATE
        SET social_media_type_name = EXCLUDED.social_media_type_name;
END;
$$;