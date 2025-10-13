
CREATE OR REPLACE FUNCTION cause_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                <> NEW.code
        OR  OLD.cause_name          <> NEW.cause_name
        OR  OLD.cause_category_id   <> NEW.cause_category_id
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
