
CREATE OR REPLACE FUNCTION social_media_type_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                    <> NEW.code
        OR  OLD.social_media_type_name  <> NEW.social_media_type_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
