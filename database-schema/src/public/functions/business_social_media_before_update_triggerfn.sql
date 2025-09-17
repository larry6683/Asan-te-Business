
CREATE OR REPLACE FUNCTION business_social_media_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.business_id                 <> NEW.business_id
        OR  OLD.social_media_type_id        <> NEW.social_media_type_id
        OR  OLD.social_media_url            <> NEW.social_media_url
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
