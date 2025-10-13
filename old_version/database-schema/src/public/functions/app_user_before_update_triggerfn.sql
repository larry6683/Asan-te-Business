
CREATE OR REPLACE FUNCTION app_user_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.email               <> NEW.email
        OR  OLD.user_type_id        <> NEW.user_type_id 
        OR  OLD.mailing_list_signup <> NEW.mailing_list_signup
    THEN
        IF lower(OLD.email) <> lower(NEW.email) THEN
            NEW.email_hash := digest(lower(NEW.email), 'md5');
        END IF;
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
