
CREATE OR REPLACE FUNCTION beneficiary_shop_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.beneficiary_id        <> NEW.beneficiary_id
        OR  OLD.shop_type_id          <> NEW.shop_type_id
        OR  OLD.shop_url              <> NEW.shop_url
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
