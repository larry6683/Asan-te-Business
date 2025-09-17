
CREATE OR REPLACE FUNCTION business_size_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                <> NEW.code
        OR  OLD.business_size_name  <> NEW.business_size_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
