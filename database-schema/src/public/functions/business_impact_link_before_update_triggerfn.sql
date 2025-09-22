
CREATE OR REPLACE FUNCTION business_impact_link_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.business_id             <>  NEW.business_id
        OR  OLD.impact_link_url         <>  NEW.impact_link_url
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
