
CREATE OR REPLACE TRIGGER registration_type_before_update_trigger
BEFORE UPDATE ON registration_type
FOR EACH ROW
EXECUTE FUNCTION registration_type_before_update_triggerfn();
