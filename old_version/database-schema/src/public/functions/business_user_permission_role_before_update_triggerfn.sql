
CREATE OR REPLACE FUNCTION business_user_permission_role_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                                <> NEW.code
        OR  OLD.business_user_permission_role_name  <> NEW.business_user_permission_role_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
