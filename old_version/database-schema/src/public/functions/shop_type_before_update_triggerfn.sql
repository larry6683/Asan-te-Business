
CREATE OR REPLACE FUNCTION shop_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code            <> NEW.code
        OR  OLD.shop_type_name  <> NEW.shop_type_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
