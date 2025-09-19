
CREATE OR REPLACE FUNCTION beneficiary_before_insert_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF NEW.beneficiary_name IS NOT NULL THEN
        NEW.beneficiary_name_hash = digest(lower(NEW.beneficiary_name), 'md5');
    END IF;
    IF NEW.email IS NOT NULL THEN
        NEW.email_hash = digest(lower(NEW.email), 'md5');
    END IF;
    RETURN NEW;
END;
$BODY$;
