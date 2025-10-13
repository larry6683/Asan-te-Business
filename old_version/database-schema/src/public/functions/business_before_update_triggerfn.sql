
CREATE OR REPLACE FUNCTION business_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.business_name           <>  NEW.business_name
        OR  OLD.email                   <>  NEW.email
        OR  OLD.website_url             <>  NEW.website_url
        OR  OLD.phone_number            <>  NEW.phone_number 
        OR  OLD.location_city           <>  NEW.location_city 
        OR  OLD.location_state          <>  NEW.location_state 
        OR  OLD.ein                     <>  NEW.ein 
        OR  OLD.business_size_id        <>  NEW.business_size_id
        OR  OLD.business_description    <>  NEW.business_description
    THEN
        IF lower(OLD.business_name) <> lower(NEW.business_name) THEN
            NEW.business_name_hash := digest(lower(NEW.business_name), 'md5');
        END IF;
        IF lower(OLD.email) <> lower(NEW.email) THEN
            NEW.email_hash := digest(lower(NEW.email), 'md5');
        END IF;
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
