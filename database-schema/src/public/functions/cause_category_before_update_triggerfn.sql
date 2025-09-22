
CREATE OR REPLACE FUNCTION cause_category_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                <> NEW.code
        OR  OLD.cause_category_name <> NEW.cause_category_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
