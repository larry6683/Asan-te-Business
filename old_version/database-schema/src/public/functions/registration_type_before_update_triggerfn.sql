
CREATE OR REPLACE FUNCTION registration_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF OLD.registration_type_name <> NEW.registration_type_name
    OR OLD.code <> NEW.code THEN
        NEW.updated_at := CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$BODY$;
