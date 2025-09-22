
CREATE OR REPLACE FUNCTION user_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code            <> NEW.code
        OR  OLD.user_type_name  <> NEW.user_type_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
