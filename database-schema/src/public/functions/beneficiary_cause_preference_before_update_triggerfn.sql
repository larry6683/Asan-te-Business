
CREATE OR REPLACE FUNCTION beneficiary_cause_preference_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.beneficiary_id                  <> NEW.beneficiary_id
        OR  OLD.cause_id                        <> NEW.cause_id
        OR  OLD.cause_preference_rank_id        <> NEW.cause_preference_rank_id
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;