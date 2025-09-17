
CREATE OR REPLACE FUNCTION beneficiary_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.beneficiary_name        <>  NEW.beneficiary_name
        OR  OLD.email                   <>  NEW.email
        OR  OLD.website_url             <>  NEW.website_url
        OR  OLD.phone_number            <>  NEW.phone_number 
        OR  OLD.location_city           <>  NEW.location_city 
        OR  OLD.location_state          <>  NEW.location_state 
        OR  OLD.ein                     <>  NEW.ein 
        OR  OLD.beneficiary_size_id     <>  NEW.beneficiary_size_id
        OR  OLD.beneficiary_description <>  NEW.beneficiary_description
    THEN
        IF lower(OLD.beneficiary_name) <> lower(NEW.beneficiary_name) THEN
            NEW.beneficiary_name_hash := digest(lower(NEW.beneficiary_name), 'md5');
        END IF;
        IF lower(OLD.email) <> lower(NEW.email) THEN
            NEW.email_hash := digest(lower(NEW.email), 'md5');
        END IF;
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
