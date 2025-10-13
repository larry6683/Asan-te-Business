
CREATE OR REPLACE FUNCTION app_user_registration_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.app_user_id         <> NEW.app_user_id
        OR  OLD.registration_type_id <> NEW.registration_type_id
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
