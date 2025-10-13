
CREATE OR REPLACE FUNCTION beneficiary_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF OLD.beneficiary_type_name <> NEW.beneficiary_type_name
    OR OLD.code <> NEW.code THEN
        NEW.updated_at := CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$BODY$;
