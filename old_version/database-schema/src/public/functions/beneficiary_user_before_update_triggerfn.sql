
CREATE OR REPLACE FUNCTION beneficiary_user_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.beneficiary_id                      <> NEW.beneficiary_id
        OR  OLD.app_user_id                         <> NEW.app_user_id
        OR  OLD.beneficiary_user_permission_role_id <> NEW.beneficiary_user_permission_role_id
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
