
CREATE OR REPLACE FUNCTION app_user_before_insert_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF NEW.email IS NOT NULL THEN
        NEW.email_hash = digest(lower(NEW.email), 'md5');
    END IF;
    RETURN NEW;
END;
$BODY$;
