
CREATE OR REPLACE FUNCTION business_user_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.business_id                         <> NEW.business_id
        OR  OLD.app_user_id                         <> NEW.app_user_id
        OR  OLD.business_user_permission_role_id    <> NEW.business_user_permission_role_id
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
