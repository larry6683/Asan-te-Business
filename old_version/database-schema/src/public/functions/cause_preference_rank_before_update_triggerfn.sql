
CREATE OR REPLACE FUNCTION cause_preference_rank_before_update_triggerfn()
RETURNS trigger
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF      OLD.code                        <> NEW.code
        OR  OLD.cause_preference_rank_name  <> NEW.cause_preference_rank_name
    THEN
        NEW.updated_at := current_timestamp;
    END IF;
    RETURN NEW;
END;
$BODY$;
