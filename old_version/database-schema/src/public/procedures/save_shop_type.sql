CREATE OR REPLACE PROCEDURE save_shop_type(
    code INT,
    shop_type_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO shop_type (code, shop_type_name)
    VALUES (code, shop_type_name)
    ON CONFLICT ON CONSTRAINT shop_type_code_key
    DO UPDATE
        SET shop_type_name = EXCLUDED.shop_type_name;
END;
$$;