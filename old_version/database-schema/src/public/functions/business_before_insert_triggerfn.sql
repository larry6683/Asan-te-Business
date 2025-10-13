
CREATE OR REPLACE FUNCTION business_before_insert_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF NEW.business_name IS NOT NULL THEN
        NEW.business_name_hash = digest(lower(NEW.business_name), 'md5');
    END IF;
    IF NEW.email IS NOT NULL THEN
        NEW.email_hash = digest(lower(NEW.email), 'md5');
    END IF;
    RETURN NEW;
END;
$BODY$;
